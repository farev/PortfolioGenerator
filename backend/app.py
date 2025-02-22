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
    linkedin: str
    about_me: str | None = None
    projects: List[dict] | None = None

class PortfolioRequest(BaseModel):
    user: UserInfo
    projects: List[Project]

class LinkedInRequest(BaseModel):
    profile_url: str

@app.post("/generate-portfolio")
async def generate_portfolio_handler(request: UserInfo):
    try:
        user_data = request.dict()
        html = generate_portfolio(user_data)
        return {"html": html}
    except Exception as e:
        logger.error(f"Portfolio generation error: {str(e)}")
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
        # Read file content
        content = await file.read()
        file_ext = file.filename.lower().split('.')[-1]
        
        # Parse based on file type
        if file_ext == 'pdf':
            data = resume_parser.parse_pdf(io.BytesIO(content))
        elif file_ext == 'docx':
            data = resume_parser.parse_docx(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        return data
    except Exception as e:
        logger.error(f"Resume parsing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-project-description")
async def generate_project_description(data: dict):
    try:
        if 'youtube_url' not in data:
            raise HTTPException(status_code=400, detail="YouTube URL is required")

        description = description_generator.generate_description(data['youtube_url'])
        if not description:
            raise HTTPException(status_code=400, detail="Could not generate description")

        return {"description": description}
    except Exception as e:
        logger.error(f"Error generating project description: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 