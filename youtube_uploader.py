"""
YouTube uploader for uploading videos with metadata.
"""

import os
import pickle
from typing import Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import get_config


class YouTubeUploader:
    """Handles YouTube video uploads."""
    
    # OAuth 2.0 scopes for YouTube upload and management
    # force-ssl allows both upload and status changes (private/public)
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    
    def __init__(self):
        self.config = get_config()
        self.youtube = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API using OAuth 2.0."""
        credentials = None
        token_path = os.path.join(self.config.temp_dir, 'youtube_token.pickle')
        
        # Try to load saved credentials
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                credentials = pickle.load(token)
        
        # If credentials don't exist or are invalid, get new ones
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing YouTube credentials...")
                credentials.refresh(Request())
            else:
                # Load client secrets
                credentials_info = self.config.get_youtube_credentials()
                
                # For GitHub Actions, we need to handle non-interactive auth
                # In production, you should have the token.pickle uploaded as a secret
                try:
                    flow = InstalledAppFlow.from_client_config(
                        credentials_info,
                        self.SCOPES
                    )
                    # Open browser for OAuth authorization
                    print("\n" + "="*80)
                    print("YOUTUBE AUTHORIZATION REQUIRED")
                    print("="*80)
                    print("Opening browser for authorization...")
                    print("If browser doesn't open, copy and paste this URL:")
                    credentials = flow.run_local_server(port=0, open_browser=True)
                    print("Authorization successful!")
                    print("="*80 + "\n")
                except Exception as e:
                    print(f"Error during OAuth flow: {e}")
                    print("For GitHub Actions, you need to pre-authorize and upload token.pickle")
                    raise
            
            # Save credentials for future use
            with open(token_path, 'wb') as token:
                pickle.dump(credentials, token)
        
        return build('youtube', 'v3', credentials=credentials)
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        thumbnail_path: Optional[str] = None,
        tags: Optional[list] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public",  # "public", "private", or "unlisted"
        publish_at: Optional[str] = None  # RFC 3339 datetime for scheduled publishing
    ) -> Optional[str]:
        """
        Upload a video to YouTube.
        
        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            thumbnail_path: Optional path to thumbnail image
            tags: Optional list of tags
            category_id: YouTube category ID (default: 22 = People & Blogs)
            privacy_status: Privacy setting (public, private, unlisted)
        
        Returns:
            Video ID if successful, None otherwise
        """
        if not os.path.exists(video_path):
            print(f"Error: Video file not found: {video_path}")
            return None
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False,
            }
        }
        
        # Add scheduled publish time if provided
        if publish_at:
            body['status']['publishAt'] = publish_at
            body['status']['privacyStatus'] = 'private'  # Must be private for scheduled publishing
            print(f"Scheduled to publish at: {publish_at}")
        
        # Check if this is a Short (vertical video under 60 seconds)
        # YouTube Shorts are automatically detected if they're vertical and under 60s
        
        print(f"Uploading to YouTube: {title}")
        if publish_at:
            print(f"Will be published publicly at: {publish_at}")
        else:
            print(f"Privacy: {privacy_status}")
        
        try:
            # Create MediaFileUpload object
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # Upload in a single request
                resumable=True,
                mimetype='video/*'
            )
            
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"Upload progress: {progress}%")
            
            video_id = response['id']
            print(f"Video uploaded successfully! Video ID: {video_id}")
            print(f"URL: https://www.youtube.com/watch?v={video_id}")
            
            # Upload thumbnail if provided
            if thumbnail_path and os.path.exists(thumbnail_path):
                self._upload_thumbnail(video_id, thumbnail_path)
            
            return video_id
            
        except Exception as e:
            print(f"Error uploading video to YouTube: {e}")
            return None
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Upload a custom thumbnail for a video.
        
        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Uploading thumbnail for video {video_id}...")
            
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
            print("Thumbnail uploaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error uploading thumbnail: {e}")
            print("Note: Custom thumbnails require account verification")
            return False
    
    def parse_tags_from_text(self, text: str) -> list:
        """
        Extract hashtags from text and convert to YouTube tags.
        
        Args:
            text: Text containing hashtags (e.g., "#podcast #tech")
        
        Returns:
            List of tags without the # symbol
        """
        words = text.split()
        tags = [word[1:] for word in words if word.startswith('#')]
        return tags

