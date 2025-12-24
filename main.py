"""
Main orchestrator for automated video uploads to YouTube and Instagram.
Runs every Tuesday and Thursday at 11 AM via GitHub Actions.
"""

import os
import sys
from datetime import datetime
from config import get_config
from metadata_manager import MetadataManager
from google_drive_handler import GoogleDriveHandler
from thumbnail_extractor import ThumbnailExtractor
from youtube_uploader import YouTubeUploader
from instagram_uploader import InstagramUploader


def cleanup_temp_files(config):
    """Clean up temporary files."""
    try:
        for file in os.listdir(config.temp_dir):
            file_path = os.path.join(config.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Cleaned up temporary files")
    except Exception as e:
        print(f"Warning: Could not clean up temp files: {e}")


def main():
    """Main execution function."""
    print("=" * 80)
    print("CINROL Video Automation System")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Initialize configuration
        print("Loading configuration...")
        config = get_config()
        print("✓ Configuration loaded")
        print()
        
        # Initialize metadata manager
        print("Connecting to Google Sheets...")
        metadata_manager = MetadataManager()
        print("✓ Connected to Google Sheets")
        print()
        
        # Get metadata for today's video
        print("Looking up video metadata...")
        metadata = metadata_manager.find_video_metadata()
        
        if not metadata:
            print("❌ No video found for today's date")
            print("Make sure your Google Sheet has:")
            print("  - A row with today's date (or Tuesday's date if today is Thursday)")
            print("  - Type column (B) set to 'Podcast'")
            print("  - Folder Name column (J) filled in")
            sys.exit(1)
        
        print("✓ Found video metadata")
        print()
        
        # Initialize Google Drive handler
        print("Connecting to Google Drive...")
        drive_handler = GoogleDriveHandler()
        print("✓ Connected to Google Drive")
        print()
        
        # Download video and cover
        print(f"Downloading video from: {metadata['folder_name']}_reels/reel_{metadata['reel_number']}/")
        video_path, cover_path = drive_handler.get_video_and_cover(
            metadata['folder_name'],
            metadata['reel_number']
        )
        
        if not video_path:
            print("❌ Failed to download video")
            sys.exit(1)
        
        print(f"✓ Downloaded video: {video_path}")
        if cover_path:
            print(f"✓ Downloaded cover: {cover_path}")
        else:
            print("ℹ No custom cover found, will extract from video")
        print()
        
        # Create/get thumbnail
        print("Preparing thumbnail...")
        thumbnail_path = ThumbnailExtractor.create_thumbnail(
            video_path,
            cover_path,
            config.temp_dir
        )
        
        if thumbnail_path:
            print(f"✓ Thumbnail ready: {thumbnail_path}")
        else:
            print("⚠ Warning: Could not create thumbnail")
        print()
        
        # Upload to YouTube
        print("-" * 80)
        print("UPLOADING TO YOUTUBE")
        print("-" * 80)
        
        try:
            youtube_uploader = YouTubeUploader()
            
            video_id = youtube_uploader.upload_video(
                video_path=video_path,
                title=metadata['youtube_title'],
                description=metadata['youtube_description'],
                thumbnail_path=thumbnail_path,
                privacy_status="public"
            )
            
            if video_id:
                print("✓ YouTube upload successful!")
                # Update status in sheet
                metadata_manager.update_status(metadata['row_number'], 'youtube', 'UPLOADED')
            else:
                print("❌ YouTube upload failed")
        except Exception as e:
            print(f"❌ YouTube upload error: {e}")
        
        print()
        
        # Upload to Instagram
        print("-" * 80)
        print("UPLOADING TO INSTAGRAM")
        print("-" * 80)
        
        try:
            instagram_uploader = InstagramUploader()
            
            media_id = instagram_uploader.upload_reel_with_retry(
                video_path=video_path,
                caption=metadata['instagram_caption'],
                cover_path=thumbnail_path,
                max_retries=3
            )
            
            if media_id:
                print("✓ Instagram upload successful!")
                # Update status in sheet
                metadata_manager.update_status(metadata['row_number'], 'instagram', 'UPLOADED')
            else:
                print("❌ Instagram upload failed")
        except Exception as e:
            print(f"❌ Instagram upload error: {e}")
        
        print()
        print("=" * 80)
        print("UPLOAD PROCESS COMPLETED")
        print("=" * 80)
        
        # Clean up
        cleanup_temp_files(config)
        
    except Exception as e:
        print()
        print("=" * 80)
        print("CRITICAL ERROR")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

