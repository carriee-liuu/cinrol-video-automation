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
from thumbnail_extractor import ThumbnailExtractor

# Instagram is optional (requires Python < 3.14)
try:
    from instagram_uploader import InstagramUploader
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False
    print("Warning: Instagram support not available (instagrapi not installed)")

# TikTok uploader (official API)
try:
    from tiktok_uploader import TikTokUploader
    TIKTOK_AVAILABLE = True
except ImportError:
    TIKTOK_AVAILABLE = False

# TikTok uploader (Buffer)
try:
    from tiktok_uploader_buffer import TikTokUploaderBuffer
    BUFFER_AVAILABLE = True
except ImportError:
    BUFFER_AVAILABLE = False


def extract_folder_id_from_link(link: str) -> Optional[str]:
    """
    Extract folder ID from Google Drive link.
    Supports formats:
    - https://drive.google.com/drive/folders/FOLDER_ID
    - https://drive.google.com/drive/u/2/folders/FOLDER_ID?...
    """
    import re
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', link)
    if match:
        return match.group(1)
    return None


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


def download_from_folder_link(drive_handler: GoogleDriveHandler, folder_link: str) -> tuple:
    """
    Download video and cover files from a Google Drive folder link.
    Returns: (video_path, cover_path)
    """
    folder_id = extract_folder_id_from_link(folder_link)
    if not folder_id:
        print(f"Error: Could not extract folder ID from link: {folder_link}")
        return None, None
    
    print(f"Folder ID: {folder_id}")
    
    # Find video file (mp4, mov, avi, mkv)
    video_file = drive_handler.find_file_in_folder(folder_id)
    if not video_file:
        print("Error: No video file found in folder")
        return None, None
    
    # Find cover file (prefer image files: png, jpg, jpeg, webp)
    # First try to find image files with "cover" or "thumbnail" in name
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    cover_file = None
    
    # Get all files in folder
    all_files = drive_handler.service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id, name, mimeType)'
    ).execute().get('files', [])
    
    # Prefer image files with "cover" or "thumbnail" in name
    for file in all_files:
        name_lower = file['name'].lower()
        ext = os.path.splitext(name_lower)[1]
        if ext in image_extensions and ('cover' in name_lower or 'thumbnail' in name_lower):
            cover_file = file
            break
    
    # If no image cover found, try any image file
    if not cover_file:
        for file in all_files:
            ext = os.path.splitext(file['name'].lower())[1]
            if ext in image_extensions:
                cover_file = file
                break
    
    # Fallback: try any file with "cover" or "thumbnail" (even if video)
    if not cover_file:
        cover_file = drive_handler.find_file_in_folder(folder_id, file_pattern="cover")
        if not cover_file:
            cover_file = drive_handler.find_file_in_folder(folder_id, file_pattern="thumbnail")
    
    config = get_config()
    
    # Download video
    video_ext = os.path.splitext(video_file['name'])[1]
    video_path = os.path.join(config.temp_dir, f"manual_video{video_ext}")
    
    if not drive_handler.download_file(video_file['id'], video_path):
        return None, None
    
    # Download cover if found
    cover_path = None
    if cover_file:
        cover_ext = os.path.splitext(cover_file['name'])[1]
        cover_path = os.path.join(config.temp_dir, f"manual_cover{cover_ext}")
        drive_handler.download_file(cover_file['id'], cover_path)
    
    return video_path, cover_path


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
    """Upload video to YouTube. Returns YouTube URL if successful."""
    print("\n" + "="*80)
    print("UPLOADING TO YOUTUBE")
    print("="*80)
    
    youtube = YouTubeUploader()
    
    # Parse schedule time if provided
    publish_at = None
    if args.schedule:
        from datetime import datetime
        import pytz
        
        try:
            # Parse the schedule time (assuming EST)
            est = pytz.timezone('America/New_York')
            naive_dt = datetime.strptime(args.schedule, '%Y-%m-%d %H:%M')
            est_dt = est.localize(naive_dt)
            
            # Convert to UTC and format as RFC 3339
            utc_dt = est_dt.astimezone(pytz.UTC)
            publish_at = utc_dt.isoformat()
            
            print(f"Scheduling for: {args.schedule} EST")
        except Exception as e:
            print(f"Error parsing schedule time: {e}")
            print("Format should be: 'YYYY-MM-DD HH:MM' (e.g., '2024-12-25 11:00')")
            return None
    
    video_id = youtube.upload_video(
        video_path=video_path,
        title=args.title,
        description=args.description,
        thumbnail_path=thumbnail_path,
        privacy_status=args.privacy or "public",
        publish_at=publish_at
    )
    
    if video_id:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"✓ YouTube upload successful!")
        print(f"  Video ID: {video_id}")
        print(f"  URL: {youtube_url}")
        if publish_at:
            print(f"  Will be published at: {args.schedule} EST")
        return youtube_url
    else:
        print("✗ YouTube upload failed")
        return None


def upload_to_instagram(args, video_path: str, cover_path: Optional[str]):
    """Upload video to Instagram. Returns Instagram URL if successful."""
    print("\n" + "="*80)
    print("UPLOADING TO INSTAGRAM - SINGLE ATTEMPT ONLY")
    print("="*80)
    
    if not INSTAGRAM_AVAILABLE:
        print("✗ Instagram support not available (requires instagrapi package)")
        return None
    
    # Additional safeguard: Check for lock file before creating uploader instance
    import hashlib
    config = get_config()
    caption_hash = hashlib.md5(args.caption.encode()).hexdigest()[:8]
    lock_file = os.path.join(config.temp_dir, f"instagram_upload_{caption_hash}.lock")
    
    if os.path.exists(lock_file):
        print(f"✗ ERROR: Lock file exists: {lock_file}")
        print("✗ Another upload with this caption is in progress or was recently completed.")
        print("✗ To prevent duplicates, this upload is BLOCKED.")
        return "locked"
    
    # Create Instagram uploader instance
    # The uploader itself has multiple safeguards built in
    instagram = InstagramUploader()
    
    # Call upload - this will only attempt once due to built-in safeguards
    print("Calling upload_reel_with_retry (which has NO retries)...")
    media_id = instagram.upload_reel_with_retry(
        video_path=video_path,
        caption=args.caption,
        cover_path=cover_path
    )
    
    if media_id and media_id != "already_attempted" and media_id != "locked" and media_id != "uploaded":
        # Try to construct Instagram URL
        # Note: instagrapi may not always return the code, so we'll try to get it
        try:
            # Try to get the media code from the client
            media_info = instagram.client.media_info(media_id)
            if hasattr(media_info, 'code'):
                instagram_url = f"https://www.instagram.com/reel/{media_info.code}/"
            else:
                instagram_url = f"https://www.instagram.com/p/{media_id}/"
        except:
            # Fallback: use media ID
            instagram_url = f"https://www.instagram.com/p/{media_id}/"
        
        print(f"✓ Instagram upload successful!")
        print(f"  Media ID: {media_id}")
        print(f"  URL: {instagram_url}")
        return instagram_url
    elif media_id == "uploaded":
        # Upload succeeded but we couldn't get the ID
        print(f"✓ Instagram upload successful!")
        print(f"  Note: Upload confirmed but URL not available")
        return "uploaded"  # Return a placeholder
    else:
        print("✗ Instagram upload failed")
        return None


def upload_to_tiktok(args, video_path: str, folder_link: str = None):
    """Upload video to TikTok using Buffer API."""
    print("\n" + "="*80)
    print("UPLOADING TO TIKTOK")
    print("="*80)
    
    # Use caption as the main text (TikTok uses caption, not separate title/description)
    caption = args.caption or args.title or "New Video"
    
    # Extract hashtags from caption
    hashtags = []
    words = caption.split()
    hashtags = [word[1:] for word in words if word.startswith('#')]
    
    # Remove hashtags from caption text (they'll be added separately)
    caption_text = " ".join([word for word in words if not word.startswith('#')])
    
    # Use Buffer (default method)
    if not BUFFER_AVAILABLE:
        print("✗ Buffer support not available")
        print("   Install: pip install requests")
        print("   Add BUFFER_ACCESS_TOKEN to .env")
        return False
    
    try:
        buffer = TikTokUploaderBuffer()
        
        # If folder link provided, use that method
        if folder_link:
            result = buffer.upload_from_google_drive_folder(
                folder_link=folder_link,
                caption=caption,
                hashtags=hashtags
            )
        else:
            # Need to get public URL for video
            print("✗ Buffer requires a public video URL or folder link")
            print("   Use --folder option or make video publicly shareable")
            return False
        
        if result:
            print(f"✓ TikTok video posted via Buffer!")
            print(f"   Post ID: {result}")
            return True
        else:
            print("✗ Buffer upload failed")
            return False
            
    except ValueError as e:
        print(f"✗ Buffer setup error: {e}")
        print("   Make sure BUFFER_ACCESS_TOKEN is in .env")
        return False
    except Exception as e:
        print(f"✗ Buffer error: {e}")
        return False


def update_instagram_bio(args):
    """Update Instagram bio links."""
    print("\n" + "="*80)
    print("UPDATING INSTAGRAM BIO")
    print("="*80)
    
    if not INSTAGRAM_AVAILABLE:
        print("✗ Instagram support not available (requires instagrapi package)")
        return False
    
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
    parser.add_argument("--video", help="Path to video file (local, drive://, or Google Drive folder link)")
    parser.add_argument("--folder", help="Google Drive folder link containing video and cover (alternative to --video and --thumbnail)")
    parser.add_argument("--thumbnail", help="Path to thumbnail/cover image (local or drive://)")
    
    # YouTube options
    parser.add_argument("--title", help="YouTube video title")
    parser.add_argument("--description", help="YouTube video description")
    parser.add_argument("--privacy", choices=["public", "private", "unlisted"], 
                       help="YouTube privacy setting (default: public)")
    parser.add_argument("--schedule", help="Schedule publish time (format: 'YYYY-MM-DD HH:MM' in EST, e.g., '2024-12-25 11:00')")
    
    # Instagram options
    parser.add_argument("--caption", help="Instagram caption")
    
    # Platform selection
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "all"], 
                       default="youtube", help="Which platform(s) to upload to")
    
    # TikTok uses Buffer API by default
    
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
    
    if not args.video and not args.folder:
        print("Error: Either --video or --folder is required")
        parser.print_help()
        sys.exit(1)
    
    if args.platform in ["youtube", "all"] and not args.title:
        print("Error: --title is required for YouTube uploads")
        sys.exit(1)
    
    if args.platform in ["instagram", "all"] and not args.caption:
        print("Error: --caption is required for Instagram uploads")
        sys.exit(1)
    
    if args.platform in ["tiktok", "all"] and not args.caption:
        print("Error: --caption is required for TikTok uploads")
        sys.exit(1)
    
    print("="*80)
    print("MANUAL VIDEO UPLOAD")
    print("="*80)
    if args.folder:
        print(f"Folder: {args.folder}")
    else:
        print(f"Video: {args.video}")
    print(f"Platform: {args.platform}")
    print()
    
    # Initialize
    config = get_config()
    drive_handler = GoogleDriveHandler()
    
    # Download video and thumbnail
    video_path = None
    thumbnail_path = None
    
    if args.folder:
        # Use folder link - automatically find video and cover
        print("Downloading from folder link...")
        video_path, thumbnail_path = download_from_folder_link(drive_handler, args.folder)
        if not video_path:
            print("Failed to download from folder")
            sys.exit(1)
    else:
        # Download video
        print("Downloading video...")
        video_path = download_from_drive(drive_handler, args.video, "manual_video.mp4")
        if not video_path:
            print("Failed to get video file")
            sys.exit(1)
        
        # Download or create thumbnail
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
    youtube_url = None
    instagram_url = None
    
    if args.platform in ["youtube", "all"]:
        youtube_url = upload_to_youtube(args, video_path, thumbnail_path)
        if not youtube_url:
            success = False
    
    if args.platform in ["instagram", "all"]:
        instagram_url = upload_to_instagram(args, video_path, thumbnail_path)
        if not instagram_url:
            success = False
    
    if args.platform in ["tiktok", "all"]:
        folder_link = args.folder if args.folder else None
        if not upload_to_tiktok(args, video_path, folder_link):
            success = False
    
    # Update Google Sheet tracker if YouTube upload succeeded
    if youtube_url and success:
        print("\n" + "="*80)
        print("UPDATING GOOGLE SHEET TRACKER")
        print("="*80)
        try:
            import subprocess
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(__file__), "update_sheet_after_post.py"),
                youtube_url
            ]
            if instagram_url and instagram_url != "uploaded":
                cmd.append(instagram_url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Google Sheet updated successfully")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"⚠ Warning: Could not update Google Sheet: {result.stderr}")
        except Exception as e:
            print(f"⚠ Warning: Error updating Google Sheet: {e}")
        print("="*80)
    
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

