# CINROL Video Automation System

Automated video upload system for Instagram Reels and YouTube Shorts/Videos. Supports both **scheduled uploads** (via local cron) and **manual/immediate uploads** via command line.

## 🎯 Features

- ✅ **Scheduled Uploads**: Automatic Tuesday/Thursday 11 AM EST uploads via local cron jobs
- ✅ **Manual Uploads**: On-demand posting from Google Drive folder links
- ✅ **Google Drive Integration**: Downloads videos and cover images automatically
- ✅ **Google Sheets Integration**: Manages metadata, titles, descriptions, and captions
- ✅ **YouTube Uploads**: Videos with custom thumbnails and scheduling support
- ✅ **Instagram Reels**: Uploads with cover images and duplicate prevention
- ✅ **TikTok Support**: Via Buffer API (optional)
- ✅ **Auto-thumbnail Extraction**: Falls back to video frames if no cover image

## 📁 Project Structure

```
cinrol-video-automation/
├── main.py                        # Scheduled upload orchestrator
├── run_automation.sh              # Cron wrapper script (runs main.py)
├── manual_upload.py               # Manual/immediate upload script
├── config.py                      # Configuration & credentials
├── metadata_manager.py            # Google Sheets integration
├── google_drive_handler.py        # Google Drive file operations
├── youtube_uploader.py            # YouTube upload functionality
├── instagram_uploader.py         # Instagram Reel uploads (duplicate prevention)
├── thumbnail_extractor.py         # Thumbnail/cover image processing
├── update_sheet_after_post.py     # Post-upload Google Sheet updates
├── requirements.txt               # Python dependencies
├── .gitignore                     # Excludes sensitive files
├── env_example.txt                # Environment variable template
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/carriee-liuu/cinrol-video-automation.git
cd cinrol-video-automation

# Install Python dependencies
pip3 install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root (copy from `env_example.txt`):

```bash
GOOGLE_SHEETS_ID=your_sheets_id
DRIVE_FOLDER_ID=your_drive_folder_id
GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
YOUTUBE_CLIENT_SECRETS='{"installed":{...}}'
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

**Important**: Never commit `.env` to git (it's in `.gitignore`)

### 3. Set Up Google Sheet

Your Google Sheet needs these columns:

| Column | Header | Required | Example |
|--------|--------|-----------|---------|
| A | what (CINROLLING) | ✅ | biggest moments of 2025 |
| B | type | ✅ | Podcast |
| C | planned publish date | ✅ | 12/23/2025 |
| J | Folder Name | ✅ | biggest moments of 2025 |
| G | long-form description | ✅ | Full description... |
| H | short-form description | ✅ | Short caption... |

### 4. Organize Google Drive

Structure your folders like this:

```
📁 Your Drive Root Folder/
  └── 📁 biggest moments of 2025/
      └── 📁 biggest moments of 2025_reels/
          ├── 📁 reel_1/  (Tuesday video)
          │   ├── video.mp4
          │   └── video_cover.jpg  (optional)
          └── 📁 reel_2/  (Thursday video)
              ├── video.mp4
              └── video_cover.jpg  (optional)
```

**Cover images**: Must contain `cover` or `thumbnail` in filename (e.g., `video_cover.jpg`, `thumbnail.png`)

## 📅 Scheduled Uploads (11 AM EST Tue/Thu)

### How It Works

The system runs automatically every **Tuesday and Thursday at 11:00 AM EST** using a local cron job on your Mac.

**Schedule Logic:**
- **Tuesday 11 AM**: Uploads `reel_1` using today's date from the sheet
- **Thursday 11 AM**: Uploads `reel_2` using Tuesday's date (2 days ago)

### Setting Up the Cron Job

The cron job is already configured. To verify or modify:

```bash
# View current cron jobs
crontab -l

# Edit cron jobs
crontab -e
```

Current cron entry:
```bash
0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

This runs at **8 AM PST** (11 AM EST) on Tuesdays and Thursdays.

### Requirements

⚠️ **Your Mac must be ON and AWAKE at 11 AM EST** on scheduled days.

To prevent sleep:
- System Settings → Lock Screen → Turn display off: Never
- Or use apps like Amphetamine or Caffeine

### What Happens During Scheduled Upload

1. Cron job triggers `run_automation.sh` at 11 AM EST
2. Script calls `main.py`
3. `main.py` reads Google Sheet to find today's video
4. Downloads video and cover from Google Drive
5. Uploads to YouTube (public, immediate)
6. Uploads to Instagram as Reel
7. Updates Google Sheet status columns
8. Logs everything to `logs/automation_YYYYMMDD_HHMMSS.log`

## 🎬 Manual/Immediate Uploads

Use `manual_upload.py` for on-demand uploads from any Google Drive folder.

### Basic Usage

```bash
# Upload to both platforms
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --title "Video Title" \
  --description "Full description..." \
  --caption "Instagram caption with #hashtags" \
  --platform all

# Instagram only
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --caption "Caption with #hashtags" \
  --platform instagram

# YouTube only
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --title "Video Title" \
  --description "Description..." \
  --platform youtube
```

### Options

- `--folder`: Google Drive folder link (required)
- `--title`: YouTube title (required for YouTube)
- `--description`: YouTube description (required for YouTube)
- `--caption`: Instagram caption (required for Instagram)
- `--platform`: `youtube`, `instagram`, `tiktok`, or `all` (default: `all`)
- `--schedule`: Schedule YouTube publish time (format: `YYYY-MM-DD HH:MM`)

### Examples

```bash
# Immediate upload to all platforms
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/16ijtvMMglqd0z2EmiztlJM_vudnH8j3b" \
  --title "My Video Title" \
  --description "Full description here" \
  --caption "Check out this video! #hashtags"

# Schedule YouTube for later (uploads as private, publishes at scheduled time)
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --title "Scheduled Video" \
  --description "Description" \
  --schedule "2026-01-30 14:00" \
  --platform youtube
```

## 🔧 API Setup Guide

### Google Drive & Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable APIs:
   - Google Drive API
   - Google Sheets API
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Name it (e.g., "video-automation")
   - Click "Create and Continue" → Skip optional steps
5. Generate Key:
   - Click on the service account → "Keys" tab → "Add Key" → "Create new key"
   - Choose JSON format → Download
6. Copy entire JSON content to `.env` as `GOOGLE_DRIVE_CREDENTIALS`
7. Share your Google Sheet and Drive folder with the service account email (found in JSON as `client_email`)

**Get Sheet ID**: From URL `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`  
**Get Drive Folder ID**: From URL `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

### YouTube Data API v3

1. In the same Google Cloud project, go to "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Configure OAuth consent screen:
   - Choose "External"
   - Fill in app name and your email
   - Add scope: `https://www.googleapis.com/auth/youtube.force-ssl`
   - Add your email as a test user
4. Create OAuth Client ID:
   - Application type: "Desktop app"
   - Name it (e.g., "YouTube Uploader")
   - Download JSON
5. Copy entire JSON content to `.env` as `YOUTUBE_CLIENT_SECRETS`

**First Run**: The script will open a browser for OAuth authorization. After authorization, a `token.pickle` file is created in `temp/` directory.

### Instagram (using instagrapi)

Simply add your Instagram credentials to `.env`:
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`

**Important**: 
- Use an Instagram Business or Creator account for best results
- Consider using a dedicated account or app-specific password
- Instagram may require 2FA verification on first login

## 🔍 Key Features Explained

### Duplicate Prevention (Instagram)

The `instagram_uploader.py` includes robust duplicate prevention:
- Class-level flag prevents multiple upload attempts per session
- Caption-based lock files prevent simultaneous uploads
- Assumes success if `clip_upload` is called (even if post-processing errors)

This ensures **one Reel per upload attempt**, preventing accidental duplicates.

### Thumbnail Handling

1. Looks for cover image in Drive folder (files with `cover` or `thumbnail` in name)
2. If found, downloads and uses as thumbnail
3. If not found, extracts frame at 1 second from video
4. Used for both YouTube thumbnail and Instagram cover

### Google Sheet Updates

After successful uploads:
- Updates status columns (E & F) to "UPLOADED"
- Adds YouTube/Instagram URLs if available
- Logs timestamps

## 📊 Character Limits

Auto-applied by the system:
- **YouTube Title**: 100 characters (truncated with "..." if longer)
- **YouTube Description**: 5,000 characters
- **Instagram Caption**: 2,200 characters (includes hashtags)

## 🧪 Testing Locally

```bash
# Test scheduled upload (reads from Google Sheet)
python3 main.py

# Test manual upload
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --title "Test" \
  --description "Test description" \
  --caption "Test caption #test" \
  --platform all
```

## 🔍 Troubleshooting

### Videos not found
- Check folder naming matches exactly (case-sensitive)
- Verify folder structure: `[Name]_reels/reel_1/` or `reel_2/`
- Confirm video files exist in the correct folders

### Sheet not updating
- Verify service account email has edit access to the sheet
- Check that Column C dates are in M/D/YYYY format
- Ensure Column B says "Podcast" (case-sensitive)

### Cron job didn't run
- Check if Mac was awake at scheduled time: `crontab -l`
- View logs: `ls -lt logs/` then `tail -20 logs/automation_*.log`
- Verify cron job exists: `crontab -l | grep run_automation`

### YouTube upload fails
- Check daily quota (10,000 units/day, ~6 uploads)
- Verify OAuth token is valid (delete `temp/youtube_token.pickle` to re-auth)
- Check video file size (max 128 GB for YouTube)

### Instagram upload fails
- Verify account is not restricted
- Check video meets requirements (max 90 seconds for Reels, MP4 format)
- Try using a business account
- Check for 2FA issues

### Duplicate Instagram posts
- The system has multiple safeguards, but if duplicates occur:
- Check lock files in `temp/` directory
- Verify only one instance of script is running
- Check logs for error messages

## 📝 Logs

- **Scheduled uploads**: `logs/automation_YYYYMMDD_HHMMSS.log`
- **Manual uploads**: Console output (or redirect to file)
- Logs are kept for 30 days (auto-cleaned by `run_automation.sh`)

## 🆘 Support

If you encounter issues:
1. Check logs for error messages
2. Verify all environment variables are set correctly
3. Test locally with `.env` file
4. Check API quotas and limits
5. Verify Mac was awake during scheduled time (for cron jobs)

## 📄 License

MIT License - feel free to modify and use for your own projects!

---

Built with ❤️ for automating content distribution
