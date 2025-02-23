from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI, APIError
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from prompts import get_portfolio_prompt, SYSTEM_PROMPT
import logging
from services.linkedin_parser import LinkedInParser
from templates.portfolio_template import generate_portfolio
from services.resume_parser import ResumeParser
import io
from services.project_generator import ProjectGenerator
from services.project_description_generator import ProjectDescriptionGenerator
from services.github_parser import extract_username, get_projects_with_description, get_user_data
from services.ai_resume_parser import AIResumeParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
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

class PortfolioRequest(BaseModel):
    user: UserInfo
    projects: List[Project]

class LinkedInRequest(BaseModel):
    profile_url: str

class GithubRequest(BaseModel):
    github_url: str

@app.post("/generate-portfolio")
async def generate_portfolio_handler(request: UserInfo):
    try:
        user_data = request.dict()
        # Add debug logs
        print("Received user_data keys:", user_data.keys())
        print("Profile image present:", "profile_image" in user_data)
        if "profile_image" in user_data:
            print("Profile image type:", type(user_data["profile_image"]))
            print("Profile image starts with:", user_data["profile_image"][:50] if user_data["profile_image"] else "None")
            
        logger.info("Generating portfolio...")
        html = generate_portfolio(user_data)
        return {"html": html}
    except Exception as e:
        logger.error(f"Portfolio generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-linkedin")
async def parse_linkedin(request: LinkedInRequest):
    try:
        parser = LinkedInParser()
        profile_data = parser.parse_profile(request.profile_url)
        return profile_data
    except Exception as e:
        logger.error(f"LinkedIn parsing error: {str(e)}")
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

        # Transform projects into portfolio format
        portfolio_projects = []
        for project in projects:
            portfolio_project = {
                "title": project["name"],
                "description": project["description"],
                "image": None,  # GitHub doesn't provide preview images
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 