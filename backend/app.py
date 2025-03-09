from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI, APIError
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from prompts import get_portfolio_prompt, SYSTEM_PROMPT
import logging
from templates.portfolio_template import generate_portfolio
from services.resume_parser import ResumeParser
import io
from services.project_generator import ProjectGenerator
from services.project_description_generator import ProjectDescriptionGenerator
from services.github_parser import extract_username, get_projects_with_description, get_user_data
from services.ai_resume_parser import AIResumeParser
from fastapi.responses import HTMLResponse
from slugify import slugify
import uuid
from storage import PortfolioStorage
import requests
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Get environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Configure origins based on environment
origins = [
    "http://localhost:3000",  # Local React development
    "http://localhost:8000",  # Local API development
    "https://folioai.tech",   # Production frontend
    "https://www.folioai.tech",
    "https://thankful-island-0de99260f.4.azurestaticapps.net"  # Azure Static Web App URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the specific origins list instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Azure OpenAI client
try:
    client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version="2024-02-15-preview"
    )
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
    raise

resume_parser = ResumeParser()

# Initialize project generator with OpenAI client
project_generator = ProjectGenerator(client)

# Initialize the description generator
description_generator = ProjectDescriptionGenerator(client)

# Initialize AI Resume parser
ai_resume_parser = AIResumeParser()

# Initialize storage
portfolio_storage = PortfolioStorage()

# Add this near your other environment variables
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

# Data validation models
class Project(BaseModel):
    title: str
    description: str
    technologies: str
    image: str | None = None

class UserInfo(BaseModel):
    name: str
    skills: str
    interests: str
    email: str
    github: str
    about_me: str | None = None
    projects: List[dict] | None = None
    linkedin: str | None = None
    profile_image: str | None = None
    profileImage: str | None = None
    html_content: str | None = None

class PortfolioRequest(BaseModel):
    user: UserInfo
    projects: List[Project]

class GithubRequest(BaseModel):
    github_url: str

@app.post("/generate-portfolio")
async def generate_portfolio_handler(request: dict):
    try:
        user_data = request.copy()
        if 'profileImage' in user_data and not user_data.get('profile_image'):
            user_data['profile_image'] = user_data.pop('profileImage')
            
        logger.info("Generating portfolio...")
        html = generate_portfolio(user_data)
        return {"html": html}
    except Exception as e:
        logger.error(f"Portfolio generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_ext = file.filename.lower().split('.')[-1]
        
        if file_ext not in ['pdf', 'docx']:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Get basic info from regular parser
        basic_data = resume_parser.parse_pdf(io.BytesIO(content)) if file_ext == 'pdf' else resume_parser.parse_docx(io.BytesIO(content))
        
        # Get enhanced content from AI parser
        ai_data = ai_resume_parser.parse_resume(io.BytesIO(content), file_ext)
        
        # Combine skills from both parsers
        all_skills = set()
        if basic_data.get('skills'):
            all_skills.update(s.strip() for s in basic_data['skills'].split(','))
        if ai_data.get('skills'):
            all_skills.update(s.strip() for s in ai_data['skills'].split(','))
        
        # Combine the data, preferring regular parser for contact info
        combined_data = {
            'name': basic_data.get('name', ''),
            'email': basic_data.get('email', ''),
            'github': basic_data.get('github', ''),
            'linkedin': basic_data.get('linkedin') or ai_data.get('linkedin', ''),
            'skills': ', '.join(sorted(all_skills)) if all_skills else ai_data.get('skills', ''),
            'interests': ai_data.get('interests', ''),
            'about_me': ai_data.get('about_me', '')
        }
        
        return combined_data
    except Exception as e:
        logger.error(f"Resume parsing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-resume-ai")
async def parse_resume_ai(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_ext = file.filename.lower().split('.')[-1]
        
        if file_ext not in ['pdf', 'docx']:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        data = ai_resume_parser.parse_resume(io.BytesIO(content), file_ext)
        return data
    except Exception as e:
        logger.error(f"AI Resume parsing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-project-description")
async def generate_project_description(data: dict):
    try:
        if not data.get('title') or not data.get('image'):
            raise HTTPException(status_code=400, detail="Title and image are required")

        description = description_generator.generate_description(
            title=data['title'],
            image=data['image'],
            brief_description=data.get('description', ''),
            youtube_url=data.get('youtube_url')
        )

        if not description:
            raise HTTPException(status_code=400, detail="Could not generate description")

        return {"description": description}
    except Exception as e:
        logger.error(f"Error generating project description: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fetch-github-projects")
async def fetch_github_projects(request: GithubRequest):
    try:
        username = extract_username(request.github_url)
        if not username:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # Get GitHub projects
        projects = get_projects_with_description(username)
        if not projects:
            return {"projects": []}

        # Tech-related search terms for more relevant images
        tech_keywords = [
            "programming", "coding", "software development",
            "computer science", "technology", "web development",
            "artificial intelligence", "data science", "cybersecurity",
            "cloud computing", "machine learning", "software engineering"
        ]

        # Transform projects into portfolio format
        portfolio_projects = []
        for project in projects:
            # Get a random tech image from Unsplash
            image_url = None
            try:
                # Use a random tech keyword for the search
                search_query = tech_keywords[len(portfolio_projects) % len(tech_keywords)]
                
                response = requests.get(
                    f"https://api.unsplash.com/photos/random",
                    params={
                        "query": search_query,
                        "orientation": "landscape",
                    },
                    headers={
                        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
                    }
                )
                
                if response.ok:
                    image_data = response.json()
                    image_url = image_data["urls"]["regular"]
            except Exception as e:
                logger.error(f"Error fetching image for project {project['name']}: {str(e)}")

            portfolio_project = {
                "title": project["name"],
                "description": project["description"],
                "image": image_url,
                "github": project["url"],
                "live": project.get("homepage"),
                "demo": None,
                "technologies": ", ".join(project.get("topics", []))
            }
            portfolio_projects.append(portfolio_project)

        return {"projects": portfolio_projects}

    except Exception as e:
        logger.error(f"Error fetching GitHub projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deploy-portfolio")
async def deploy_portfolio(request: dict):
    try:
        # Extract HTML content and user info
        html_content = request.get('html_content')
        user_info = {k: v for k, v in request.items() if k != 'html_content'}
        
        # Check if a portfolio with same GitHub or LinkedIn exists
        existing_portfolio = portfolio_storage.find_portfolio(
            github_url=user_info.get('github'),
            linkedin_url=user_info.get('linkedin')
        )
        
        if existing_portfolio and existing_portfolio.get('slug'):
            # Update existing portfolio
            slug = existing_portfolio['slug']
            logger.info(f"Updating existing portfolio with slug: {slug}")
        else:
            # Create new portfolio
            base_slug = slugify(user_info.get('name', 'portfolio'))  # Provide default name
            slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            logger.info(f"Creating new portfolio with slug: {slug}")
        
        # Save the portfolio with all user info
        portfolio_storage.save_portfolio(slug, {
            "html_content": html_content,
            "github_url": user_info.get('github'),
            "linkedin_url": user_info.get('linkedin'),
            "name": user_info.get('name'),
            "email": user_info.get('email'),
            "about_me": user_info.get('about_me'),
            "skills": user_info.get('skills'),
            "interests": user_info.get('interests'),
            "profile_image": user_info.get('profile_image'),
            "projects": user_info.get('projects', []),
            "slug": slug
        })
        
        # Generate the portfolio URL
        portfolio_url = f"/{slug}"
        
        return {
            "url": portfolio_url,
            "slug": slug
        }
    except Exception as e:
        logger.error(f"Portfolio deployment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/{slug}")
async def get_portfolio(slug: str):
    html_content = portfolio_storage.get_portfolio(slug)
    if not html_content:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/check-portfolio")
async def check_portfolio(request: dict):
    try:
        linkedin_url = request.get('linkedin')
        if not linkedin_url:
            return {"exists": False}
            
        existing_portfolio = portfolio_storage.find_portfolio(linkedin_url=linkedin_url)
        if existing_portfolio:
            return {
                "exists": True,
                "portfolio": {
                    "name": existing_portfolio.get("name"),
                    "email": existing_portfolio.get("email"),
                    "github": existing_portfolio.get("github_url"),
                    "linkedin": existing_portfolio.get("linkedin_url"),
                    "about_me": existing_portfolio.get("about_me"),
                    "skills": existing_portfolio.get("skills"),
                    "interests": existing_portfolio.get("interests"),
                    "profile_image": existing_portfolio.get("profile_image"),
                    "projects": existing_portfolio.get("projects", []),
                    "slug": existing_portfolio.get("slug")
                },
                "html": existing_portfolio.get("html_content")
            }
        return {"exists": False}
    except Exception as e:
        logger.error(f"Error checking portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 