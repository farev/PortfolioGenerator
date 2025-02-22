import requests
import os
import logging
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)

class LinkedInParser:
    def __init__(self):
        self.api = Linkedin(
            os.getenv('LINKEDIN_USERNAME'),
            os.getenv('LINKEDIN_PASSWORD')
        )

    def parse_profile(self, linkedin_url):
        try:
            # Extract username from URL
            username = linkedin_url.split('/in/')[-1].split('/')[0]
            
            # Get profile data
            profile = self.api.get_profile(username)
            experiences = self.api.get_profile_experience(username)
            skills = self.api.get_profile_skills(username)
            
            # Calculate years of experience
            years_experience = len(experiences) if experiences else 0
            
            return {
                'name': f"{profile.get('firstName', '')} {profile.get('lastName', '')}",
                'profession': profile.get('headline', ''),
                'years_experience': years_experience,
                'skills': ', '.join([skill['name'] for skill in skills]) if skills else '',
                'about_me': profile.get('summary', ''),
                'linkedin': linkedin_url
            }
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn profile: {str(e)}")
            raise 