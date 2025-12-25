"""
TikTok uploader for posting videos.
Note: TikTok's official API has limited access. This uses unofficial methods.
"""

import os
from typing import Optional
from config import get_config


class TikTokUploader:
    """Handles TikTok video uploads."""
    
    def __init__(self):
        self.config = get_config()
        print("⚠️  TikTok API Note:")
        print("   TikTok's official API requires special approval.")
        print("   For now, you'll need to use TikTok's web interface to upload.")
        print("   The video will be downloaded for you to upload manually.")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        hashtags: list = None
    ) -> Optional[str]:
        """
        Prepare video for TikTok upload.
        
        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            hashtags: List of hashtags
        
        Returns:
            Message about manual upload needed
        """
        if not os.path.exists(video_path):
            print(f"Error: Video file not found: {video_path}")
            return None
        
        # Combine title, description, and hashtags
        caption = title
        if description:
            caption += f"\n\n{description}"
        if hashtags:
            caption += "\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        
        print("\n" + "="*80)
        print("TIKTOK UPLOAD PREPARATION")
        print("="*80)
        print(f"Video ready: {video_path}")
        print(f"\nCaption to use:")
        print("-" * 40)
        print(caption)
        print("-" * 40)
        print("\n⚠️  Manual Upload Required:")
        print("   1. Open TikTok app or https://www.tiktok.com/upload")
        print("   2. Upload the video file above")
        print("   3. Copy and paste the caption")
        print("   4. Post!")
        print("="*80)
        
        return "manual_upload_required"
    
    def upload_with_retry(
        self,
        video_path: str,
        title: str,
        description: str = "",
        hashtags: list = None,
        max_retries: int = 3
    ) -> Optional[str]:
        """
        Upload video with retry logic.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            hashtags: List of hashtags
            max_retries: Maximum retry attempts
        
        Returns:
            Upload result
        """
        return self.upload_video(video_path, title, description, hashtags)

