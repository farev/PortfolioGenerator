import json
import os
import logging

logger = logging.getLogger(__name__)

class PortfolioStorage:
    def __init__(self):
        self.storage_dir = os.path.join(os.path.dirname(__file__), 'portfolios')
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def save_portfolio(self, slug: str, data: dict):
        try:
            # Save JSON data
            json_path = os.path.join(self.storage_dir, f"{slug}.json")
            portfolio_data = {
                "html_content": data.get("html_content"),
                "github_url": data.get("github_url"),
                "linkedin_url": data.get("linkedin_url"),
                "name": data.get("name"),
                "email": data.get("email"),
                "about_me": data.get("about_me"),
                "skills": data.get("skills"),
                "interests": data.get("interests"),
                "profile_image": data.get("profile_image"),
                "projects": data.get("projects", []),
                "slug": slug
            }
            with open(json_path, 'w') as f:
                json.dump(portfolio_data, f)

            # Save HTML content separately
            html_path = os.path.join(self.storage_dir, f"{slug}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(data.get("html_content", ""))

            logger.info(f"Saved portfolio data to {json_path} and HTML to {html_path}")
        except Exception as e:
            logger.error(f"Error saving portfolio: {str(e)}")
            raise
            
    def get_portfolio(self, slug: str) -> str:
        try:
            # Try to get HTML from dedicated HTML file first
            html_path = os.path.join(self.storage_dir, f"{slug}.html")
            if os.path.exists(html_path):
                with open(html_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # Fall back to JSON if HTML file doesn't exist
            json_path = os.path.join(self.storage_dir, f"{slug}.json")
            with open(json_path, 'r') as f:
                data = json.load(f)
                return data.get('html_content')
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error getting portfolio: {str(e)}")
            return None

    def find_portfolio(self, github_url: str = None, linkedin_url: str = None) -> dict:
        if not github_url and not linkedin_url:
            return None

        try:
            # Search through all portfolio files
            for filename in os.listdir(self.storage_dir):
                if not filename.endswith('.json'):
                    continue
                    
                file_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                        # Check if either GitHub or LinkedIn URLs match
                        if github_url and data.get('github_url') == github_url:
                            logger.info(f"Found portfolio by GitHub URL: {filename}")
                            return data
                        if linkedin_url and data.get('linkedin_url') == linkedin_url:
                            logger.info(f"Found portfolio by LinkedIn URL: {filename}")
                            return data
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in file: {filename}")
                    continue
                    
            logger.info("No matching portfolio found")
            return None
            
        except Exception as e:
            logger.error(f"Error finding portfolio: {str(e)}")
            return None 