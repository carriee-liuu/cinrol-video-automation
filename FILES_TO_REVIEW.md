# Files Ready to Push to Git

## 📋 Overview

This repository contains working scripts for:
1. **Scheduled uploads** at 11 AM EST (Tuesday/Thursday) via **local cron jobs** (Mac must be awake)
2. **Manual/immediate uploads** via command line

## 📁 Files to Push (13 Essential Files)

### 1. Scheduled Uploads (11 AM EST)
- **main.py** - Main orchestrator
  - Reads video metadata from Google Sheets
  - Downloads from Google Drive (`folder_name_reels/reel_1` or `reel_2`)
  - Uploads to YouTube & Instagram
  - Updates Google Sheet status

- **run_automation.sh** - Local cron job wrapper script
  - Runs via local cron: `0 8 * * 2,4` (8 AM PST = 11 AM EST Tue/Thu)
  - Calls `main.py` and logs output
  - Requires Mac to be ON and AWAKE at scheduled time

### 2. Manual/Immediate Uploads
- **manual_upload.py** - Command-line upload script
  - Usage: `python manual_upload.py --folder "DRIVE_LINK" --title "..." --caption "..." --platform all`
  - Supports Google Drive folder links
  - Uploads to YouTube, Instagram, TikTok (via Buffer)
  - Updates Google Sheet after successful uploads

### 3. Supporting Core Modules
- **config.py** - Configuration management
  - Loads credentials from environment variables
  - Supports `.env` file for local testing
  - Validates character limits

- **google_drive_handler.py** - Google Drive operations
  - Downloads videos and cover images
  - Supports folder-by-name and folder-by-ID lookups
  - Used by both `main.py` and `manual_upload.py`

- **youtube_uploader.py** - YouTube uploads
  - OAuth 2.0 authentication
  - Uploads videos with thumbnails
  - Supports scheduling (private → public at specific time)

- **instagram_uploader.py** - Instagram Reel uploads
  - Uses `clip_upload` to ensure Reels (not posts)
  - Multiple duplicate prevention mechanisms:
    - Class-level `_upload_attempted` flag
    - Caption-based lock files
    - Assumes success if `clip_upload` succeeds (even if post-processing errors)

- **thumbnail_extractor.py** - Thumbnail processing
  - Extracts frames from videos
  - Processes cover images
  - Creates YouTube thumbnails

- **metadata_manager.py** - Google Sheets integration
  - Reads video metadata (title, description, caption)
  - Updates upload status
  - Finds videos by date

- **update_sheet_after_post.py** - Post-upload updates
  - Updates Google Sheet with YouTube/Instagram URLs
  - Adds rows to "Posting Schedule" if needed

- **run_automation.sh** - Local cron wrapper script
  - Wrapper for `main.py` that runs via cron
  - Handles logging and error tracking
  - Used for scheduled Tuesday/Thursday uploads

### 4. Configuration Files
- **requirements.txt** - Python dependencies
  - google-api-python-client, instagrapi, opencv-python, etc.

- **.gitignore** - Excludes sensitive files
  - `.env`, `temp/`, `*.pickle`, `instagram_session.json`, etc.

## 🔒 Files NOT Included (Security)
- `.env` - Contains all API credentials
- `temp/` - Temporary downloaded files
- `*.pickle` - OAuth tokens
- `instagram_session.json` - Instagram session data
- `youtube_token_base64.txt` - YouTube token backup

## ✅ Key Features

### Scheduled Uploads (main.py + run_automation.sh)
- Runs automatically via LOCAL cron job (not GitHub Actions)
- Cron schedule: `0 8 * * 2,4` (8 AM PST = 11 AM EST Tue/Thu)
- Reads from Google Sheets (finds video by date)
- Downloads from structured Drive folders
- Uploads to both platforms
- Updates sheet status
- Requires Mac to be ON and AWAKE at scheduled time

### Manual Uploads (manual_upload.py)
- Supports Google Drive folder links directly
- Flexible platform selection (youtube, instagram, all)
- Can schedule YouTube videos for future publish
- Updates Google Sheet tracker after uploads

## 🚀 Usage Examples

### Scheduled (Automatic)
- Runs every Tuesday/Thursday at 11 AM EST via local cron
- Cron job: `0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh`
- Mac must be ON and AWAKE at scheduled time
- No action needed - fully automated (if Mac is awake)

### Manual Upload
```bash
# Upload from Google Drive folder link
python manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --title "Video Title" \
  --description "Video description..." \
  --caption "Instagram caption with #hashtags" \
  --platform all
```

## 📝 Next Steps

Ready to push these files to:
`https://github.com/carriee-liuu/cinrol-video-automation.git`

All files are working and tested. The `.gitignore` ensures sensitive files are excluded.
