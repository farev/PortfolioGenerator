from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI, APIError
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from prompts import get_portfolio_prompt, SYSTEM_PROMPT
import logging
from services.linkedin_parser import LinkedInParser

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

# Data validation models
class Project(BaseModel):
    title: str
    description: str
    technologies: str
    image: str | None = None

class UserInfo(BaseModel):
    name: str
    profession: str
    years_experience: int
    skills: str
    interests: str
    hobbies: str
    email: str
    github: str
    linkedin: str
    about_me: str | None = None

class PortfolioRequest(BaseModel):
    user: UserInfo
    projects: List[Project]

class LinkedInRequest(BaseModel):
    profile_url: str

@app.post("/generate-portfolio")
async def generate_portfolio(request: PortfolioRequest):
    try:
        prompt = get_portfolio_prompt(request.user, request.projects)
        logger.info("Generated prompt successfully")

        try:
            response = client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=999,
            )
            
            generated_html = response.choices[0].message.content
            logger.info("Successfully generated HTML response")
            
            return {"html": generated_html}
        
        except APIError as e:
            logger.error(f"Azure OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Azure OpenAI API error: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 