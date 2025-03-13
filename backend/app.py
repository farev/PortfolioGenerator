from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI, APIError
from pydantic import BaseModel
from typing import List, Optional
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
from database import get_db
from database import User, Portfolio
from services.db_service import DatabaseService
import requests
from urllib.parse import quote
from sqlalchemy.orm import Session
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Get environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Get Unsplash API key
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
if not UNSPLASH_ACCESS_KEY:
    logger.warning("UNSPLASH_ACCESS_KEY not found in environment variables")

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

# Create database tables on startup
@app.on_event("startup")
def startup_db_client():
    from database import create_tables
    create_tables()

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
async def generate_portfolio_endpoint(data: dict, db: Session = Depends(get_db)):
    try:
        user_data = data.copy()
        if 'profileImage' in user_data and not user_data.get('profile_image'):
            user_data['profile_image'] = user_data.pop('profileImage')
            
        logger.info("Generating portfolio...")
        
        # Check if a portfolio already exists for this user's LinkedIn or GitHub
        existing_portfolio = None
        if data.get('linkedin'):
            existing_portfolio = DatabaseService.find_portfolio_by_urls(db, None, data.get('linkedin'))
            if existing_portfolio:
                logger.info(f"Found existing portfolio with slug: {existing_portfolio.slug}")
        
        if not existing_portfolio and data.get('github'):
            existing_portfolio = DatabaseService.find_portfolio_by_urls(db, data.get('github'), None)
            if existing_portfolio:
                logger.info(f"Found existing portfolio with slug: {existing_portfolio.slug}")

        html = generate_portfolio(user_data)
        
        # If we found an existing portfolio, update it instead of creating a new one
        if existing_portfolio:
            # Update the portfolio content
            existing_portfolio.html_content = html
            existing_portfolio.about_me = data.get('about_me', '')
            existing_portfolio.interests = data.get('interests', '')
            
            # Update projects if needed
            if data.get('projects'):
                existing_portfolio.projects = json.dumps(data.get('projects', []))
            
            # Update the user
            user = existing_portfolio.user
            if data.get('name'):
                user.name = data.get('name')
            if data.get('skills'):
                user.skills = data.get('skills')
            if data.get('email'):
                user.email = data.get('email')
            if data.get('github'):
                user.github_url = data.get('github')
            if data.get('linkedin'):
                user.linkedin_url = data.get('linkedin')
            
            # Commit the changes
            db.commit()
            db.refresh(existing_portfolio)
            logger.info(f"Updated existing portfolio with slug: {existing_portfolio.slug}")
            
            # Return the updated portfolio
            return {
                "slug": existing_portfolio.slug,
                "html_content": html
            }
        
        # Create a unique slug for the portfolio
        name = data.get('name', '')
        slug = f"{slugify(name)}-{str(uuid.uuid4())[:8]}" if name else f"portfolio-{str(uuid.uuid4())[:8]}"
        
        # Save portfolio data
        portfolio_data = {
            "html_content": html,
            "github_url": data.get('github', ''),
            "linkedin_url": data.get('linkedin', ''),
            "name": data.get('name', ''),
            "email": data.get('email', ''),
            "about_me": data.get('about_me', ''),
            "skills": data.get('skills', ''),
            "interests": data.get('interests', ''),
            "profile_image": data.get('profile_image', ''),
            "projects": data.get('projects', []),
            "slug": slug
        }
        
        # Save user and portfolio to database
        user = DatabaseService.get_or_create_user(db, {
            "name": data.get('name', ''),
            "email": data.get('email', ''),
            "linkedin": data.get('linkedin', ''),
            "github": data.get('github', ''),
            "skills": data.get('skills', '')
        })
        
        portfolio = DatabaseService.save_portfolio(db, user.id, portfolio_data)
        slug = portfolio.slug
        
        # Return the generated portfolio
        return {
            "slug": slug,
            "html_content": html
        }
    except Exception as e:
        logger.error(f"Portfolio generation error: {str(e)}")
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
async def deploy_portfolio(request: dict, db: Session = Depends(get_db)):
    try:
        # Extract HTML content and user info
        html_content = request.get('html_content')
        user_info = {k: v for k, v in request.items() if k != 'html_content'}
        
        # Check if there's an existing portfolio with the same LinkedIn or GitHub URL
        existing_portfolio = None
        
        # First check by LinkedIn URL
        if user_info.get('linkedin'):
            linkedin_portfolio = DatabaseService.find_portfolio_by_urls(db, None, user_info.get('linkedin'))
            if linkedin_portfolio:
                existing_portfolio = linkedin_portfolio
                logger.info(f"Found existing portfolio by LinkedIn URL with slug: {existing_portfolio.slug}")
        
        # Then check by GitHub URL if no portfolio was found by LinkedIn
        if not existing_portfolio and user_info.get('github'):
            github_portfolio = DatabaseService.find_portfolio_by_urls(db, user_info.get('github'), None)
            if github_portfolio:
                existing_portfolio = github_portfolio
                logger.info(f"Found existing portfolio by GitHub URL with slug: {existing_portfolio.slug}")
        
        # If we found an existing portfolio, update it instead of creating a new one
        if existing_portfolio:
            slug = existing_portfolio.slug
            logger.info(f"Updating existing portfolio with slug: {slug}")
            
            # Update the portfolio content
            existing_portfolio.html_content = html_content
            existing_portfolio.about_me = user_info.get('about_me', '')
            existing_portfolio.interests = user_info.get('interests', '')
            
            # Update projects if needed
            if user_info.get('projects'):
                existing_portfolio.projects = json.dumps(user_info.get('projects'))
            
            # Update the user
            user = existing_portfolio.user
            if user_info.get('name'):
                user.name = user_info.get('name')
            if user_info.get('skills'):
                user.skills = user_info.get('skills')
            if user_info.get('email'):
                user.email = user_info.get('email')
            if user_info.get('github'):
                user.github_url = user_info.get('github')
            if user_info.get('linkedin'):
                user.linkedin_url = user_info.get('linkedin')
            
            # Commit the changes
            db.commit()
            db.refresh(existing_portfolio)
            logger.info(f"Successfully updated portfolio {slug} in database")
            
            # Generate the portfolio URL
            portfolio_url = f"/{slug}"
            
            return {
                "url": portfolio_url,
                "slug": slug
            }
        
        # First, try to find the user by LinkedIn, GitHub, or email
        user = None
        if user_info.get('linkedin'):
            user_by_linkedin = db.query(User).filter(User.linkedin_url == user_info.get('linkedin')).first()
            if user_by_linkedin:
                user = user_by_linkedin
        
        if not user and user_info.get('github'):
            user_by_github = db.query(User).filter(User.github_url == user_info.get('github')).first()
            if user_by_github:
                user = user_by_github
        
        if not user and user_info.get('email'):
            user_by_email = db.query(User).filter(User.email == user_info.get('email')).first()
            if user_by_email:
                user = user_by_email
        
        # Create new portfolio
        base_slug = slugify(user_info.get('name', 'portfolio'))  # Provide default name
        slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
        logger.info(f"Creating new portfolio with slug: {slug}")
        
        # Save the portfolio with all user info
        portfolio_data = {
            "html_content": html_content,
            "about_me": user_info.get('about_me', ''),
            "interests": user_info.get('interests', ''),
            "projects": user_info.get('projects', []),
            "slug": slug
        }
        
        # Save user and portfolio to database
        user = DatabaseService.get_or_create_user(db, {
            "name": user_info.get('name', ''),
            "email": user_info.get('email', ''),
            "linkedin": user_info.get('linkedin', ''),
            "github": user_info.get('github', ''),
            "skills": user_info.get('skills', '')
        })
        
        portfolio = DatabaseService.save_portfolio(db, user.id, portfolio_data)
        slug = portfolio.slug
        
        # Generate the portfolio URL
        portfolio_url = f"/{slug}"
        
        return {
            "url": portfolio_url,
            "slug": slug
        }
    except Exception as e:
        logger.error(f"Portfolio deployment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/{slug}", response_class=HTMLResponse)
async def get_portfolio(slug: str, db: Session = Depends(get_db)):
    try:
        portfolio = DatabaseService.get_portfolio_by_slug(db, slug)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Log portfolio details for debugging
        logger.info(f"Retrieved portfolio {slug}")
        
        # If we need to process the portfolio before returning it
        # For example, if the template needs projects as a list instead of a JSON string
        if portfolio.projects:
            try:
                projects_list = json.loads(portfolio.projects)
                # You might need to update your template to use this data
                # Or you might need to regenerate the HTML with the updated projects
                logger.info(f"Portfolio has {len(projects_list)} projects")
            except Exception as e:
                logger.error(f"Error parsing projects JSON: {str(e)}")
        
        # Create response with no-cache headers
        response = HTMLResponse(content=portfolio.html_content, status_code=200)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-portfolio")
async def check_portfolio(request: dict, db: Session = Depends(get_db)):
    try:
        linkedin_url = request.get('linkedin')
        if not linkedin_url:
            return {"exists": False}
            
        existing_portfolio = DatabaseService.find_portfolio_by_urls(db, request.get('github'), linkedin_url)
        if existing_portfolio:
            # Get the user associated with this portfolio
            user = existing_portfolio.user
            
            # Get projects as a list (convert from JSON string)
            projects = json.loads(existing_portfolio.projects) if existing_portfolio.projects else []
            
            return {
                "exists": True,
                "portfolio": {
                    "name": user.name,
                    "email": user.email,
                    "github": user.github_url,
                    "linkedin": user.linkedin_url,
                    "about_me": existing_portfolio.about_me,
                    "skills": user.skills,
                    "interests": existing_portfolio.interests,
                    "projects": projects,
                    "slug": existing_portfolio.slug
                },
                "html": existing_portfolio.html_content
            }
        return {"exists": False}
    except Exception as e:
        logger.error(f"Error checking portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/find-portfolio")
async def find_portfolio(github_url: str = None, linkedin_url: str = None, db: Session = Depends(get_db)):
    try:
        if not github_url and not linkedin_url:
            raise HTTPException(status_code=400, detail="Either GitHub or LinkedIn URL is required")
        
        portfolio = DatabaseService.find_portfolio_by_urls(db, github_url, linkedin_url)
        
        if not portfolio:
            return {"found": False}
        
        return {
            "found": True,
            "slug": portfolio.slug
        }
    except Exception as e:
        logger.error(f"Error finding portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-project/{slug}")
async def add_project(slug: str, project: dict, db: Session = Depends(get_db)):
    try:
        # Find the portfolio
        portfolio = DatabaseService.get_portfolio_by_slug(db, slug)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Get existing projects
        existing_projects = []
        if portfolio.projects:
            try:
                existing_projects = json.loads(portfolio.projects)
            except:
                logger.warning(f"Could not parse existing projects for portfolio {slug}")
        
        # Add the new project
        existing_projects.append(project)
        
        # Update the portfolio
        portfolio.projects = json.dumps(existing_projects)
        db.commit()
        
        # Regenerate the HTML with the updated projects
        user = portfolio.user
        portfolio_data = {
            "name": user.name,
            "email": user.email,
            "github": user.github_url,
            "linkedin": user.linkedin_url,
            "about_me": portfolio.about_me,
            "skills": user.skills,
            "interests": portfolio.interests,
            "profile_image": project.get('profile_image'),  # Get profile image from project data
            "projects": existing_projects
        }
        
        # Generate new HTML
        html_content = generate_portfolio(portfolio_data)
        
        # Update the portfolio HTML
        portfolio.html_content = html_content
        db.commit()
        
        # Force a refresh of the portfolio from the database
        db.refresh(portfolio)
        logger.info(f"Successfully added project to portfolio {slug} and updated HTML")
        
        return {"success": True, "project_count": len(existing_projects)}
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 