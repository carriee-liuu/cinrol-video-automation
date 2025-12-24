"""
Configuration management for video automation system.
Loads credentials and settings from environment variables and GitHub secrets.
"""

import os
import json
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists (for local testing)
load_dotenv()


class Config:
    """Configuration class for managing API credentials and settings."""
    
    def __init__(self):
        # Google Sheets ID
        self.sheets_id = os.getenv('GOOGLE_SHEETS_ID')
        if not self.sheets_id:
            raise ValueError("GOOGLE_SHEETS_ID environment variable is required")
        
        # Google Drive folder ID (root folder containing all podcast folders)
        self.drive_folder_id = os.getenv('DRIVE_FOLDER_ID')
        if not self.drive_folder_id:
            raise ValueError("DRIVE_FOLDER_ID environment variable is required")
        
        # Google credentials (service account JSON)
        self.google_credentials_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        if not self.google_credentials_json:
            raise ValueError("GOOGLE_DRIVE_CREDENTIALS environment variable is required")
        
        # YouTube credentials (OAuth client secrets JSON)
        self.youtube_credentials_json = os.getenv('YOUTUBE_CLIENT_SECRETS')
        if not self.youtube_credentials_json:
            raise ValueError("YOUTUBE_CLIENT_SECRETS environment variable is required")
        
        # Instagram credentials (using instagrapi)
        self.instagram_username = os.getenv('INSTAGRAM_USERNAME')
        self.instagram_password = os.getenv('INSTAGRAM_PASSWORD')
        
        if not self.instagram_username or not self.instagram_password:
            raise ValueError("INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD are required")
        
        # Platform character limits
        self.youtube_title_max = 100
        self.youtube_description_max = 5000
        self.instagram_caption_max = 2200
        
        # Timezone (default to UTC, adjust as needed)
        self.timezone = os.getenv('TIMEZONE', 'America/New_York')
        
        # Temp directory for downloads
        self.temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def get_google_credentials(self) -> dict:
        """Parse and return Google credentials as a dictionary."""
        return json.loads(self.google_credentials_json)
    
    def get_youtube_credentials(self) -> dict:
        """Parse and return YouTube credentials as a dictionary."""
        return json.loads(self.youtube_credentials_json)
    
    def truncate_text(self, text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to max length with optional suffix."""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    def validate_youtube_title(self, title: str) -> str:
        """Validate and truncate YouTube title."""
        return self.truncate_text(title, self.youtube_title_max)
    
    def validate_youtube_description(self, description: str) -> str:
        """Validate and truncate YouTube description."""
        if len(description) <= self.youtube_description_max:
            return description
        return description[:self.youtube_description_max]
    
    def validate_instagram_caption(self, caption: str) -> str:
        """Validate and truncate Instagram caption."""
        if len(caption) <= self.instagram_caption_max:
            return caption
        return caption[:self.instagram_caption_max]


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the configuration singleton."""
    global _config
    if _config is None:
        _config = Config()
    return _config

