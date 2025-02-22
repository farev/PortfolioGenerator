import logging
from typing import Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class ProjectGenerator:
    def __init__(self, client: AzureOpenAI):
        self.client = client

    def _extract_github_info(self, github_url: str) -> Dict:
        """Extract information from GitHub repository."""
        try:
            # Parse the URL to get owner and repo
            path = urlparse(github_url).path
            owner, repo = path.strip('/').split('/')[-2:]
            
            # Use GitHub API
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url)
            if response.ok:
                data = response.json()
                return {
                    'description': data.get('description', ''),
                    'languages': list(data.get('languages_url', {}).keys()),
                    'stars': data.get('stargazers_count', 0),
                    'forks': data.get('forks_count', 0)
                }
        except Exception as e:
            logger.error(f"Error extracting GitHub info: {str(e)}")
        return {}

    def _extract_youtube_info(self, youtube_url: str) -> str:
        """Extract information from YouTube video."""
        try:
            response = requests.get(youtube_url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                description = soup.find('meta', {'name': 'description'})
                return description.get('content', '') if description else ''
        except Exception as e:
            logger.error(f"Error extracting YouTube info: {str(e)}")
        return ''

    def generate_description(self, project_data: Dict) -> Dict:
        """Generate project description using available information."""
        context = []

        # Collect information from different sources
        if project_data.get('github'):
            github_info = self._extract_github_info(project_data['github'])
            if github_info:
                context.append(f"GitHub repository information: {github_info}")

        if project_data.get('demo'):
            youtube_info = self._extract_youtube_info(project_data['demo'])
            if youtube_info:
                context.append(f"Project demo information: {youtube_info}")

        # Generate prompt
        prompt = f"""Generate a detailed project description for a portfolio website. Use the following information:

Project Title: {project_data['title']}

Available Links:
- GitHub: {project_data.get('github', 'Not provided')}
- Demo: {project_data.get('demo', 'Not provided')}
- Live: {project_data.get('live', 'Not provided')}

Additional Context:
{' '.join(context)}

Please provide:
1. A comprehensive project description
2. A list of technologies used (extracted or inferred)
"""

        try:
            response = self.client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a technical writer helping to create portfolio project descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            # Parse the response
            content = response.choices[0].message.content
            description_match = re.search(r'Description:(.*?)(?=Technologies|$)', content, re.DOTALL)
            technologies_match = re.search(r'Technologies:(.*?)$', content, re.DOTALL)
            
            return {
                'description': description_match.group(1).strip() if description_match else content,
                'technologies': technologies_match.group(1).strip() if technologies_match else ''
            }

        except Exception as e:
            logger.error(f"Error generating project description: {str(e)}")
            raise 