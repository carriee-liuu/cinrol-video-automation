"""
YouTube video publisher - Changes video from private to public.
Use this for scheduled Shorts publishing.
"""

import sys
from youtube_uploader import YouTubeUploader


def publish_video(video_id: str) -> bool:
    """
    Change a video from private to public.
    
    Args:
        video_id: YouTube video ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Publishing video {video_id}...")
        
        uploader = YouTubeUploader()
        
        # Update video status to public
        uploader.youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }
        ).execute()
        
        print(f"✓ Video is now PUBLIC!")
        print(f"  URL: https://www.youtube.com/watch?v={video_id}")
        return True
        
    except Exception as e:
        print(f"✗ Error publishing video: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 publish_video.py VIDEO_ID")
        print("Example: python3 publish_video.py uNcI8cbleGM")
        sys.exit(1)
    
    video_id = sys.argv[1]
    success = publish_video(video_id)
    sys.exit(0 if success else 1)

