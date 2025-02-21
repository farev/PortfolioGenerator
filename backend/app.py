from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

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
client = AzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version="2024-02-15-preview"
)

# Data validation models
class Project(BaseModel):
    title: str
    description: str
    technologies: str
    image: str | None = None

class ProjectsRequest(BaseModel):
    projects: List[Project]

@app.post("/generate-portfolio")
async def generate_portfolio(request: ProjectsRequest):
    try:
        # Construct the prompt for the LLM
        prompt = """Generate a modern, responsive HTML portfolio page for the following projects. 
        Include CSS styling within a <style> tag. The design should be professional and minimal.
        
        Projects:
        """
        
        for project in request.projects:
            prompt += f"\nTitle: {project.title}\n"
            prompt += f"Description: {project.description}\n"
            prompt += f"Technologies: {project.technologies}\n"
            prompt += "---"

        response = client.chat.completions.create(
            model=os.getenv('AZURE_OPENAI_MODEL'),
            messages=[
                {"role": "system", "content": "You are a professional web developer who creates clean, modern portfolio websites."},
                {"role": "user", "content": prompt}
            ]
        )
        
        generated_html = response.choices[0].message.content
        
        return {"html": generated_html}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 