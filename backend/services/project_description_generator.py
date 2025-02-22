import logging
import re
from typing import Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class ProjectDescriptionGenerator:
    def __init__(self, client: AzureOpenAI):
        self.client = client

    def extract_youtube_info(self, url: str) -> Dict:
        """Extract information from a YouTube video."""
        try:
            # Extract video ID from URL
            parsed_url = urlparse(url)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            elif parsed_url.hostname == 'youtu.be':
                video_id = parsed_url.path[1:]
            else:
                return None

            if not video_id:
                return None

            # Get video page
            response = requests.get(f'https://www.youtube.com/watch?v={video_id}')
            if not response.ok:
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract video metadata
            title = soup.find('meta', property='og:title')
            description = soup.find('meta', property='og:description')
            
            return {
                'title': title.get('content', '') if title else '',
                'description': description.get('content', '') if description else '',
                'video_id': video_id
            }
        except Exception as e:
            logger.error(f"Error extracting YouTube info: {str(e)}")
            return None

    def generate_description(self, youtube_url: str) -> str:
        """Generate a project description from a YouTube video."""
        try:
            video_info = self.extract_youtube_info(youtube_url)
            if not video_info:
                return None

            prompt = f"""Based on this YouTube video information, generate a professional project description:

Title: {video_info['title']}
Video Description: {video_info['description']}

Please provide a concise but detailed description that:
1. Explains the project's purpose and main features
2. Highlights key technical aspects
3. Describes the user experience
4. Mentions any notable achievements or innovations

Keep the tone professional and focus on the technical aspects."""

            response = self.client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a technical writer helping to create project descriptions for a developer portfolio."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            return None 