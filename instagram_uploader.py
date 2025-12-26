"""
Instagram uploader for uploading Reels with captions and cover images.
"""

import os
import time
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, FeedbackRequired
from config import get_config


class InstagramUploader:
    """Handles Instagram Reels uploads using instagrapi."""
    
    def __init__(self):
        self.config = get_config()
        self.client = Client()
        self.session_file = os.path.join(self.config.temp_dir, 'instagram_session.json')
        self._login()
    
    def _login(self):
        """Login to Instagram using credentials."""
        # Try to load existing session
        if os.path.exists(self.session_file):
            try:
                print("Loading Instagram session...")
                self.client.load_settings(self.session_file)
                self.client.login(
                    self.config.instagram_username,
                    self.config.instagram_password
                )
                
                # Verify session is valid
                self.client.get_timeline_feed()
                print("Instagram session loaded successfully")
                return
            except Exception as e:
                print(f"Existing session invalid: {e}")
        
        # Perform fresh login
        try:
            print(f"Logging into Instagram as {self.config.instagram_username}...")
            self.client.login(
                self.config.instagram_username,
                self.config.instagram_password
            )
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            print("Instagram login successful")
            
        except ChallengeRequired as e:
            print("Instagram requires verification (2FA or challenge)")
            print(f"Error: {e}")
            raise Exception(
                "Instagram challenge required. Please verify your account manually "
                "or use an account without 2FA for automation."
            )
        except LoginRequired as e:
            print(f"Instagram login failed: {e}")
            raise Exception("Instagram login failed. Check your credentials.")
        except Exception as e:
            print(f"Error logging into Instagram: {e}")
            raise
    
    def upload_reel(
        self,
        video_path: str,
        caption: str,
        cover_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload a video as an Instagram Reel.
        
        Args:
            video_path: Path to the video file
            caption: Caption text (including hashtags)
            cover_path: Optional path to cover image
        
        Returns:
            Media ID if successful, None otherwise
        """
        if not os.path.exists(video_path):
            print(f"Error: Video file not found: {video_path}")
            return None
        
        # Validate video duration (Instagram Reels max 90 seconds)
        # Note: instagrapi will handle this, but we can add a check if needed
        
        print(f"Uploading Reel to Instagram...")
        print(f"Caption: {caption[:100]}..." if len(caption) > 100 else f"Caption: {caption}")
        
        try:
            # Upload video as Reel (using video_upload which is more reliable)
            media = self.client.video_upload(
                path=video_path,
                caption=caption,
                thumbnail=cover_path if cover_path and os.path.exists(cover_path) else None
            )
            
            media_id = media.pk
            print(f"Reel uploaded successfully! Media ID: {media_id}")
            print(f"URL: https://www.instagram.com/reel/{media.code}/")
            
            return str(media_id)
            
        except FeedbackRequired as e:
            print(f"Instagram feedback required: {e}")
            print("Your account may be flagged for spam or automation. Wait before trying again.")
            return None
        except Exception as e:
            print(f"Error uploading Reel to Instagram: {e}")
            return None
    
    def upload_reel_with_retry(
        self,
        video_path: str,
        caption: str,
        cover_path: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: int = 60
    ) -> Optional[str]:
        """
        Upload Reel with automatic retry on failure.
        
        Args:
            video_path: Path to the video file
            caption: Caption text
            cover_path: Optional path to cover image
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        
        Returns:
            Media ID if successful, None otherwise
        """
        for attempt in range(1, max_retries + 1):
            print(f"Upload attempt {attempt}/{max_retries}")
            
            try:
                result = self.upload_reel(video_path, caption, cover_path)
                if result:
                    return result
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
            
            if attempt < max_retries:
                print(f"Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
        
        print("All upload attempts failed")
        return None
    
    def append_hashtags(self, caption: str, hashtags: str) -> str:
        """
        Append hashtags to caption if not already present.
        
        Args:
            caption: Original caption text
            hashtags: Hashtags to append (space-separated)
        
        Returns:
            Caption with hashtags
        """
        if not hashtags:
            return caption
        
        # Check if hashtags are already in caption
        caption_lower = caption.lower()
        for tag in hashtags.split():
            if tag.lower() not in caption_lower:
                caption += f" {tag}"
        
        return caption

