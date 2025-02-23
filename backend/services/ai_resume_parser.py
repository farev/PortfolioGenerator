from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Dict
import PyPDF2
import docx
import re

logger = logging.getLogger(__name__)

class AIResumeParser:
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version="2024-02-15-preview"
        )

    def _extract_text(self, file_content: bytes, file_type: str) -> str:
        """Extract text from PDF or DOCX file."""
        try:
            if file_type == 'pdf':
                pdf_reader = PyPDF2.PdfReader(file_content)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            elif file_type == 'docx':
                doc = docx.Document(file_content)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                return text
        except Exception as e:
            logger.error(f"Error extracting text from {file_type}: {str(e)}")
            raise

    def _preprocess_text(self, text: str) -> str:
        """Preprocess and summarize resume text to reduce tokens."""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Extract most important sections using common resume section headers
        important_sections = {
            'summary': r'(?i)(summary|objective|profile|about).*?(?=\n\n|\Z)',
            'experience': r'(?i)(experience|work history).*?(?=\n\n|\Z)',
            'skills': r'(?i)(skills|technologies|competencies).*?(?=\n\n|\Z)',
            'education': r'(?i)(education|academic).*?(?=\n\n|\Z)'
        }
        
        extracted_text = []
        for section, pattern in important_sections.items():
            matches = re.search(pattern, text, re.DOTALL)
            if matches:
                # Take first 200 characters of each section
                section_text = matches.group(0)[:200]
                extracted_text.append(section_text)
        
        # Join sections and limit to ~800 characters total
        summarized_text = ' '.join(extracted_text)[:800]
        return summarized_text

    def _analyze_with_ai(self, text: str) -> Dict:
        """Use Azure OpenAI to analyze the resume text."""
        # Preprocess and summarize text
        summarized_text = self._preprocess_text(text)
        
        prompt = f"""Analyze this resume summary and extract key information:
SKILLS: List main technical and professional skills
INTERESTS: List key interests and passions
LINKEDIN: Extract LinkedIn URL if present
ABOUT_ME: Write 1-2 sentences about the person

Resume Summary:
{summarized_text}

Format response exactly as:
SKILLS: <skills list>
INTERESTS: <interests list>
LINKEDIN: <URL or 'Not found'>
ABOUT_ME: <summary>"""

        try:
            response = self.client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a resume analyzer. Be brief and precise."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300  # Further limit response length
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Extract sections using regex
            skills_match = re.search(r'SKILLS: (.*?)(?=\n|$)', content)
            interests_match = re.search(r'INTERESTS: (.*?)(?=\n|$)', content)
            linkedin_match = re.search(r'LINKEDIN: (.*?)(?=\n|$)', content)
            about_match = re.search(r'ABOUT_ME: (.*?)(?=\n|$)', content)
            
            return {
                'skills': skills_match.group(1).strip() if skills_match else '',
                'interests': interests_match.group(1).strip() if interests_match else '',
                'linkedin': linkedin_match.group(1).strip() if linkedin_match and 'not found' not in linkedin_match.group(1).lower() else '',
                'about_me': about_match.group(1).strip() if about_match else ''
            }

        except Exception as e:
            logger.error(f"Error analyzing resume with AI: {str(e)}")
            raise

    def parse_resume(self, file_content: bytes, file_type: str) -> Dict:
        """Main method to parse resume and extract information using AI."""
        try:
            # First extract text from the file
            text = self._extract_text(file_content, file_type)
            
            # Then analyze with AI
            parsed_data = self._analyze_with_ai(text)
            
            return parsed_data

        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise 