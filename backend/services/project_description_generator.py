import logging
import re
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import base64
from io import BytesIO
from PIL import Image
import os
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class ProjectDescriptionGenerator:
    def __init__(self, client: AzureOpenAI):
        self.client = client
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum time between requests in seconds

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def _generate_with_openai(self, prompt: str, max_tokens: int = 200) -> str:
        """Make API call to OpenAI with retry logic"""
        self._wait_for_rate_limit()
        
        response = self.client.chat.completions.create(
            model=os.getenv('AZURE_OPENAI_MODEL'),
            messages=[
                {"role": "system", "content": "You are a technical writer helping to enhance project descriptions for a developer portfolio. Provide only the description text without any headers or labels."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()

    def _process_image_for_analysis(self, image_data: str) -> str:
        """Process base64 image data to ensure it's in a suitable format."""
        try:
            # Remove data URL prefix if present
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            # Decode base64, open image and resize if too large
            img_bytes = base64.b64decode(image_data)
            img = Image.open(BytesIO(img_bytes))
            
            # Resize if image is too large (max 1024x1024)
            max_size = 1024
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)))
            
            # Convert back to base64
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return image_data

    def generate_description(self, title: str, image: str, brief_description: str = "", **kwargs) -> str:
        """Generate a project description based on image and user input."""
        try:
            processed_image = self._process_image_for_analysis(image)
            
            prompt = f"""Based on this project information, provide a concise enhanced description:

Project Title: {title}
User's Description: {brief_description}

Please provide a brief but detailed description that:
1. Builds upon the user's description
2. Adds key technical details based on the image
3. Maintains the original context
4. Uses a professional tone

Keep it concise (2-5 sentences) but technically informative."""

            description = self._generate_with_openai(prompt)
            
            # Clean up the response by removing any title/description headers
            description = re.sub(r'^(Project Title:|Description:|Title:).*?\n', '', description, flags=re.MULTILINE)
            return description.strip()

        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            return brief_description  # Return original description if generation fails 