import PyPDF2
import docx
import logging
import re
import spacy
from typing import Dict, List
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx']
        # Load English language model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Download if not available
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # Common section headers
        self.section_headers = {
            'skills': r'(?i)(technical\s+)?skills?|technologies|competencies|expertise',
            'experience': r'(?i)experience|employment( history)?|work history|work experience',
            'projects': r'(?i)projects?|portfolio|works',
            'education': r'(?i)education|academic|qualification',
            'summary': r'(?i)summary|objective|profile|about',
        }

        # Common programming languages and technologies
        self.tech_keywords = set([
            'python', 'java', 'javascript', 'js', 'typescript', 'ts', 'c++', 'c#',
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'aws', 'azure',
            'docker', 'kubernetes', 'git', 'ci/cd', 'rest', 'graphql',
            'html', 'css', 'sass', 'less', 'webpack', 'babel', 'jquery',
            'machine learning', 'ai', 'artificial intelligence', 'data science',
            'tensorflow', 'pytorch', 'keras', 'opencv', 'nlp'
        ])

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the text using regex patterns."""
        sections = {}
        lines = text.split('\n')
        current_section = 'unknown'
        section_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a section header
            is_header = False
            for section, pattern in self.section_headers.items():
                if re.match(pattern, line, re.IGNORECASE):
                    if section_content:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = section
                    section_content = []
                    is_header = True
                    break

            if not is_header:
                section_content.append(line)

        # Add the last section
        if section_content:
            sections[current_section] = '\n'.join(section_content)

        return sections

    def _extract_name(self, text: str) -> str:
        """Extract name using NER and heuristics."""
        # Try to find name at the beginning of the resume
        first_lines = text.split('\n')[:3]
        doc = self.nlp(' '.join(first_lines))
        
        # Look for PERSON entities
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return ent.text

        # Fallback: Take the first line if it looks like a name
        first_line = first_lines[0].strip()
        if len(first_line.split()) <= 4 and not any(char.isdigit() for char in first_line):
            return first_line

        return ''

    def _extract_skills(self, text: str, sections: Dict[str, str]) -> List[str]:
        """Extract skills using keyword matching and NLP."""
        skills = set()
        
        # Look in skills section first
        if 'skills' in sections:
            skills_text = sections['skills']
            # Split by common delimiters
            skill_candidates = re.split(r'[,|•|\n]', skills_text)
            
            for skill in skill_candidates:
                skill = skill.strip().lower()
                # Match against known technologies
                if skill in self.tech_keywords:
                    skills.add(skill)
                # Look for technology patterns
                elif re.search(r'\b[A-Za-z]+(?:\+\+|#|\.js|\.NET)?\b', skill):
                    skills.add(skill)

        # Look for skills in other sections
        doc = self.nlp(text)
        for token in doc:
            if token.text.lower() in self.tech_keywords:
                skills.add(token.text.lower())

        return list(skills)

    def _extract_experience(self, sections: Dict[str, str]) -> List[Dict]:
        """Extract work experience entries."""
        experiences = []
        if 'experience' not in sections:
            return experiences

        experience_text = sections['experience']
        # Split into entries (assuming entries are separated by double newlines)
        entries = re.split(r'\n\s*\n', experience_text)

        for entry in entries:
            # Try to extract company and position
            lines = entry.strip().split('\n')
            if not lines:
                continue

            experience = {}
            
            # Look for dates
            date_pattern = r'(?i)(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}\s*-\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}|present|current'
            dates = re.findall(date_pattern, entry)
            if dates:
                experience['duration'] = dates[0]

            # First line usually contains position and/or company
            position_company = lines[0].strip()
            experience['title'] = position_company

            # Look for description in remaining lines
            description = ' '.join(lines[1:])
            experience['description'] = description.strip()

            if experience:
                experiences.append(experience)

        return experiences

    def _extract_projects(self, sections: Dict[str, str]) -> List[Dict]:
        """Extract project information."""
        projects = []
        if 'projects' not in sections:
            return projects

        project_text = sections['projects']
        # Split into individual projects
        project_entries = re.split(r'\n\s*\n', project_text)

        for entry in project_entries:
            lines = entry.strip().split('\n')
            if not lines:
                continue

            project = {}
            
            # First line is usually the project title
            project['title'] = lines[0].strip()

            # Look for technologies used
            tech_used = []
            for line in lines:
                for tech in self.tech_keywords:
                    if tech in line.lower():
                        tech_used.append(tech)
            
            if tech_used:
                project['technologies'] = ', '.join(tech_used)

            # Remaining lines are description
            project['description'] = ' '.join(lines[1:]).strip()

            if project:
                projects.append(project)

        return projects

    def _extract_information(self, text: str) -> Dict:
        # Clean the text
        text = re.sub(r'\s+', ' ', text)
        
        # Extract sections
        sections = self._extract_sections(text)
        
        # Extract information
        name = self._extract_name(text)
        skills = self._extract_skills(text, sections)
        experiences = self._extract_experience(sections)
        projects = self._extract_projects(sections)
        
        # Extract email using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, text)
        email = email_matches[0] if email_matches else ''

        # Build about me from summary section
        about_me = sections.get('summary', '')
        if not about_me and experiences:
            # Use most recent experience as fallback
            about_me = experiences[0].get('description', '')

        return {
            'name': name,
            'email': email,
            'skills': ', '.join(skills),
            'about_me': about_me,
            'experiences': experiences,
            'projects': projects,
            'interests': self._extract_interests(text)
        }

    def _extract_interests(self, text: str) -> str:
        """Extract interests and hobbies."""
        interests_pattern = r'(?i)interests|hobbies'
        matches = re.split(interests_pattern, text)
        if len(matches) > 1:
            # Take the text after the "interests" keyword until the next section
            interests_text = matches[1].split('\n\n')[0]
            return interests_text.strip()
        return ''

    def parse_pdf(self, file_content: bytes) -> Dict:
        try:
            pdf_reader = PyPDF2.PdfReader(file_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return self._extract_information(text)
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise

    def parse_docx(self, file_content: bytes) -> Dict:
        try:
            doc = docx.Document(file_content)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return self._extract_information(text)
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            raise 