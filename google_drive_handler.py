"""
Google Drive handler for downloading videos and cover images.
"""

import os
import io
from typing import Optional, Tuple
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from config import get_config


class GoogleDriveHandler:
    """Handles all Google Drive operations."""
    
    def __init__(self):
        self.config = get_config()
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API using service account."""
        credentials_info = self.config.get_google_credentials()
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)
    
    def find_folder_by_name(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Find a folder by name within a parent folder.
        
        Args:
            folder_name: Name of the folder to find
            parent_id: Parent folder ID (uses root folder from config if None)
        
        Returns:
            Folder ID if found, None otherwise
        """
        if parent_id is None:
            parent_id = self.config.drive_folder_id
        
        query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        
        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=10
            ).execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            return None
        except Exception as e:
            print(f"Error finding folder '{folder_name}': {e}")
            return None
    
    def find_file_in_folder(self, folder_id: str, file_pattern: Optional[str] = None) -> Optional[dict]:
        """
        Find a file in a folder, optionally matching a pattern.
        
        Args:
            folder_id: Folder ID to search in
            file_pattern: Optional pattern to match (e.g., '_cover' for cover images)
        
        Returns:
            Dict with file info (id, name) if found, None otherwise
        """
        query = f"'{folder_id}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
        
        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType)',
                pageSize=50
            ).execute()
            
            files = results.get('files', [])
            
            if file_pattern:
                # Filter files matching the pattern
                matching_files = [f for f in files if file_pattern in f['name']]
                if matching_files:
                    return matching_files[0]
                return None
            else:
                # Return first video file
                video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
                for f in files:
                    if any(f['name'].lower().endswith(ext) for ext in video_extensions):
                        return f
                return None
        except Exception as e:
            print(f"Error finding file in folder: {e}")
            return None
    
    def download_file(self, file_id: str, destination_path: str) -> bool:
        """
        Download a file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save the file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            with io.FileIO(destination_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"Download progress: {int(status.progress() * 100)}%")
            
            print(f"Downloaded file to: {destination_path}")
            return True
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False
    
    def get_video_and_cover(
        self, 
        folder_name: str, 
        reel_number: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Download video and cover image for a specific reel.
        
        Args:
            folder_name: Name of the podcast folder (from Google Sheet Column J)
            reel_number: 1 for Tuesday, 2 for Thursday
        
        Returns:
            Tuple of (video_path, cover_path). Either can be None if not found.
        """
        # Build the path: [folder_name]_reels/reel_1 or reel_2
        reels_folder_name = f"{folder_name}_reels"
        reel_folder_name = f"reel_{reel_number}"
        
        print(f"Looking for: {reels_folder_name}/{reel_folder_name}")
        
        # Find the _reels folder
        reels_folder_id = self.find_folder_by_name(reels_folder_name)
        if not reels_folder_id:
            print(f"Error: Could not find folder '{reels_folder_name}'")
            return None, None
        
        # Find the reel_X folder
        reel_folder_id = self.find_folder_by_name(reel_folder_name, reels_folder_id)
        if not reel_folder_id:
            print(f"Error: Could not find folder '{reel_folder_name}' inside '{reels_folder_name}'")
            return None, None
        
        print(f"Found reel folder: {reel_folder_name}")
        
        # Find video file
        video_file = self.find_file_in_folder(reel_folder_id)
        if not video_file:
            print(f"Error: No video file found in '{reel_folder_name}'")
            return None, None
        
        # Find cover image (optional)
        cover_file = self.find_file_in_folder(reel_folder_id, file_pattern='_cover')
        
        # Download video
        video_ext = os.path.splitext(video_file['name'])[1]
        video_path = os.path.join(self.config.temp_dir, f"video_{reel_number}{video_ext}")
        
        if not self.download_file(video_file['id'], video_path):
            return None, None
        
        # Download cover if exists
        cover_path = None
        if cover_file:
            cover_ext = os.path.splitext(cover_file['name'])[1]
            cover_path = os.path.join(self.config.temp_dir, f"cover_{reel_number}{cover_ext}")
            
            if not self.download_file(cover_file['id'], cover_path):
                print(f"Warning: Failed to download cover image, will extract from video")
                cover_path = None
        else:
            print(f"No cover image found (looking for files with '_cover' in name)")
        
        return video_path, cover_path

