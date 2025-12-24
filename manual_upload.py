"""
Manual video upload script for Instagram and YouTube.
Run on-demand from command line whenever you want to upload content.

Usage Examples:
    # Instagram only
    python manual_upload.py --video "drive://folder/video.mp4" \\
        --caption "New episode! 🎙️ #podcast" \\
        --platform instagram

    # YouTube only
    python manual_upload.py --video "drive://folder/video.mp4" \\
        --title "Episode 4: Big Moments" \\
        --description "Full episode description..." \\
        --thumbnail "drive://folder/cover.jpg" \\
        --platform youtube

    # Both platforms
    python manual_upload.py --video "drive://folder/video.mp4" \\
        --title "Episode 4" \\
        --description "..." \\
        --caption "New episode!" \\
        --thumbnail "drive://folder/cover.jpg" \\
        --platform both

    # Update Instagram bio only
    python manual_upload.py --update-bio \\
        --episode 4 \\
        --spotify-url "https://open.spotify.com/..." \\
        --youtube-url "https://youtu.be/..."
"""

import argparse
import os
import sys
from typing import Optional

from config import get_config
from google_drive_handler import GoogleDriveHandler
from youtube_uploader import YouTubeUploader
from instagram_uploader import InstagramUploader
from thumbnail_extractor import ThumbnailExtractor


def parse_drive_path(path: str) -> tuple:
    """
    Parse Google Drive path in format: drive://folder_name/file_name
    Returns: (folder_name, file_name)
    """
    if path.startswith("drive://"):
        path = path[8:]  # Remove "drive://"
        parts = path.split("/")
        if len(parts) >= 2:
            return "/".join(parts[:-1]), parts[-1]
    return None, path


def download_from_drive(drive_handler: GoogleDriveHandler, drive_path: str, local_filename: str) -> Optional[str]:
    """Download a file from Google Drive given a path."""
    folder_path, filename = parse_drive_path(drive_path)
    
    if not folder_path:
        # It's a local file
        if os.path.exists(drive_path):
            return drive_path
        else:
            print(f"Error: File not found: {drive_path}")
            return None
    
    print(f"Downloading from Google Drive: {folder_path}/{filename}")
    
    # Navigate to folder
    folder_id = drive_handler.config.drive_folder_id
    for folder_name in folder_path.split("/"):
        folder_id = drive_handler.find_folder_by_name(folder_name, folder_id)
        if not folder_id:
            print(f"Error: Folder not found: {folder_name}")
            return None
    
    # Find file
    file_info = drive_handler.find_file_in_folder(folder_id, file_pattern=None)
    if not file_info or file_info['name'] != filename:
        # Try to find exact filename
        results = drive_handler.service.files().list(
            q=f"name='{filename}' and '{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        if not files:
            print(f"Error: File not found: {filename}")
            return None
        file_info = files[0]
    
    # Download
    config = get_config()
    local_path = os.path.join(config.temp_dir, local_filename)
    
    if drive_handler.download_file(file_info['id'], local_path):
        return local_path
    
    return None


def upload_to_youtube(args, video_path: str, thumbnail_path: Optional[str]):
    """Upload video to YouTube."""
    print("\n" + "="*80)
    print("UPLOADING TO YOUTUBE")
    print("="*80)
    
    youtube = YouTubeUploader()
    
    video_id = youtube.upload_video(
        video_path=video_path,
        title=args.title,
        description=args.description,
        thumbnail_path=thumbnail_path,
        privacy_status=args.privacy or "public"
    )
    
    if video_id:
        print(f"✓ YouTube upload successful!")
        print(f"  Video ID: {video_id}")
        print(f"  URL: https://www.youtube.com/watch?v={video_id}")
        return True
    else:
        print("✗ YouTube upload failed")
        return False


def upload_to_instagram(args, video_path: str, cover_path: Optional[str]):
    """Upload video to Instagram."""
    print("\n" + "="*80)
    print("UPLOADING TO INSTAGRAM")
    print("="*80)
    
    instagram = InstagramUploader()
    
    media_id = instagram.upload_reel_with_retry(
        video_path=video_path,
        caption=args.caption,
        cover_path=cover_path
    )
    
    if media_id:
        print(f"✓ Instagram upload successful!")
        print(f"  Media ID: {media_id}")
        return True
    else:
        print("✗ Instagram upload failed")
        return False


def update_instagram_bio(args):
    """Update Instagram bio links."""
    print("\n" + "="*80)
    print("UPDATING INSTAGRAM BIO")
    print("="*80)
    
    instagram = InstagramUploader()
    
    try:
        # Update bio with episode links
        bio_text = f"nyc, 20s, and pretending we know what we're doing\nnew episode every tuesday 🎙️"
        
        # Update bio
        instagram.client.account_edit(
            biography=bio_text
        )
        
        # Set external links
        links = [
            {
                "link_type": "external",
                "url": args.spotify_url,
                "title": f"episode {args.episode} on spotify"
            },
            {
                "link_type": "external", 
                "url": args.youtube_url,
                "title": f"episode {args.episode} on youtube"
            }
        ]
        
        instagram.client.account_set_biography_links(links)
        
        print(f"✓ Instagram bio updated with episode {args.episode} links!")
        return True
    except Exception as e:
        print(f"✗ Failed to update bio: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Manual video upload to Instagram and YouTube",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Video upload options
    parser.add_argument("--video", help="Path to video file (local or drive://folder/file.mp4)")
    parser.add_argument("--thumbnail", help="Path to thumbnail/cover image (local or drive://)")
    
    # YouTube options
    parser.add_argument("--title", help="YouTube video title")
    parser.add_argument("--description", help="YouTube video description")
    parser.add_argument("--privacy", choices=["public", "private", "unlisted"], 
                       help="YouTube privacy setting (default: public)")
    
    # Instagram options
    parser.add_argument("--caption", help="Instagram caption")
    
    # Platform selection
    parser.add_argument("--platform", choices=["youtube", "instagram", "both"], 
                       default="both", help="Which platform(s) to upload to")
    
    # Bio update options
    parser.add_argument("--update-bio", action="store_true", 
                       help="Update Instagram bio (instead of uploading video)")
    parser.add_argument("--episode", type=int, help="Episode number for bio")
    parser.add_argument("--spotify-url", help="Spotify episode URL")
    parser.add_argument("--youtube-url", help="YouTube episode URL")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.update_bio:
        if not all([args.episode, args.spotify_url, args.youtube_url]):
            print("Error: --update-bio requires --episode, --spotify-url, and --youtube-url")
            sys.exit(1)
        
        success = update_instagram_bio(args)
        sys.exit(0 if success else 1)
    
    if not args.video:
        print("Error: --video is required")
        parser.print_help()
        sys.exit(1)
    
    if args.platform in ["youtube", "both"] and not args.title:
        print("Error: --title is required for YouTube uploads")
        sys.exit(1)
    
    if args.platform in ["instagram", "both"] and not args.caption:
        print("Error: --caption is required for Instagram uploads")
        sys.exit(1)
    
    print("="*80)
    print("MANUAL VIDEO UPLOAD")
    print("="*80)
    print(f"Video: {args.video}")
    print(f"Platform: {args.platform}")
    print()
    
    # Initialize
    config = get_config()
    drive_handler = GoogleDriveHandler()
    
    # Download video
    print("Downloading video...")
    video_path = download_from_drive(drive_handler, args.video, "manual_video.mp4")
    if not video_path:
        print("Failed to get video file")
        sys.exit(1)
    
    # Download or create thumbnail
    thumbnail_path = None
    if args.thumbnail:
        print("Downloading thumbnail...")
        thumbnail_path = download_from_drive(drive_handler, args.thumbnail, "manual_thumbnail.jpg")
    else:
        print("No thumbnail provided, extracting from video...")
        thumbnail_path = ThumbnailExtractor.create_thumbnail(
            video_path, None, config.temp_dir
        )
    
    # Upload to platforms
    success = True
    
    if args.platform in ["youtube", "both"]:
        if not upload_to_youtube(args, video_path, thumbnail_path):
            success = False
    
    if args.platform in ["instagram", "both"]:
        if not upload_to_instagram(args, video_path, thumbnail_path):
            success = False
    
    # Cleanup
    print("\nCleaning up temporary files...")
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
        if thumbnail_path and os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
    except:
        pass
    
    print("\n" + "="*80)
    if success:
        print("✓ UPLOAD COMPLETED SUCCESSFULLY")
    else:
        print("✗ UPLOAD COMPLETED WITH ERRORS")
    print("="*80)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

