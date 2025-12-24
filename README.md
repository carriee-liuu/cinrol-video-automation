# CINROL Video Automation System

Automated video upload system for Instagram Reels and YouTube Shorts/Videos. Runs automatically every Tuesday and Thursday at 11 AM, pulling videos from Google Drive and metadata from Google Sheets.

## 🎯 Features

- ✅ Automated Tuesday/Thursday 11 AM uploads
- ✅ Google Drive integration for video storage
- ✅ Google Sheets for metadata management
- ✅ YouTube upload with custom thumbnails
- ✅ Instagram Reels upload with cover images
- ✅ Custom cover image support
- ✅ Auto-thumbnail extraction fallback
- ✅ Runs free on GitHub Actions

## 📁 Project Structure

```
video-automation/
├── .github/
│   └── workflows/
│       └── upload_videos.yml     # Scheduler
├── config.py                      # Configuration
├── metadata_manager.py            # Google Sheets integration
├── google_drive_handler.py        # Drive downloads
├── youtube_uploader.py            # YouTube uploads
├── instagram_uploader.py          # Instagram uploads
├── thumbnail_extractor.py         # Thumbnail generation
├── main.py                        # Main orchestrator
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Create GitHub Repository

1. Create a new repository on GitHub (public or private)
2. Clone this code to your local machine
3. Push to your repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Set Up Google Sheet

Add **Column J: "Folder Name"** to your existing sheet:

| Column | Header | Example |
|--------|--------|---------|
| A | what (CINROLLING) | biggest moments of 2025 |
| B | type | Podcast |
| C | planned publish date | 12/23/2025 |
| D | Files link | (manual reference) |
| E | YT/spotify | UPLOADED |
| F | IG/YT shorts | UPLOADED |
| G | long-form description | Join as we discuss... |
| H | short-form description | New episode! 🎙️ |
| I | short desc 2 | (optional) |
| **J** | **Folder Name** | **biggest moments of 2025** |

### 3. Organize Google Drive

Structure your folders like this:

```
📁 Your Drive Folder/
  └── 📁 biggest moments of 2025/
      └── 📁 biggest moments of 2025_reels/
          ├── 📁 reel_1/  (Tuesday video)
          │   ├── video.mp4
          │   └── video_cover.jpg  (optional)
          └── 📁 reel_2/  (Thursday video)
              ├── video.mp4
              └── video_cover.jpg  (optional)
```

**Important**: Cover images must end with `_cover` (e.g., `video_cover.jpg`, `thumbnail_cover.png`)

### 4. Set Up API Credentials

See **[API Setup Guide](#-api-setup-guide)** below for detailed instructions.

### 5. Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

| Secret Name | Description |
|-------------|-------------|
| `GOOGLE_SHEETS_ID` | Your Google Sheet ID (from the URL) |
| `DRIVE_FOLDER_ID` | Root folder ID in Google Drive |
| `GOOGLE_DRIVE_CREDENTIALS` | Service account JSON (entire file as text) |
| `YOUTUBE_CLIENT_SECRETS` | OAuth client secrets JSON |
| `INSTAGRAM_USERNAME` | Your Instagram username |
| `INSTAGRAM_PASSWORD` | Your Instagram password |

### 6. Adjust Schedule (Optional)

Edit `.github/workflows/upload_videos.yml`:

```yaml
schedule:
  - cron: '0 15 * * 2,4'  # 11 AM EST = 15:00 UTC (adjust for your timezone)
```

## 📅 How It Works

### Schedule Logic

- **Tuesday 11 AM**: Uploads `reel_1` using today's date in the sheet
- **Thursday 11 AM**: Uploads `reel_2` using Tuesday's date (2 days ago)

### Example Flow

1. **Tuesday, Dec 24, 2025 @ 11 AM**:
   - Script looks for row with date `12/24/2025` in Column C
   - Gets folder name from Column J: `biggest moments of 2025`
   - Navigates to: `biggest moments of 2025_reels/reel_1/`
   - Downloads video and cover image
   - Uploads to YouTube with title (Column A) and description (Column G)
   - Uploads to Instagram with caption (Column H)
   - Updates status in Columns E & F

2. **Thursday, Dec 26, 2025 @ 11 AM**:
   - Script looks for row with date `12/24/2025` (2 days ago)
   - Uses same folder: `biggest moments of 2025_reels/reel_2/`
   - Uploads second reel from the same episode

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
   - Click "Create and Continue"
   - Skip optional steps
5. Generate Key:
   - Click on the service account you created
   - Go to "Keys" tab → "Add Key" → "Create new key"
   - Choose JSON format
   - Download the JSON file
6. Copy the entire JSON content to GitHub secret `GOOGLE_DRIVE_CREDENTIALS`
7. Share your Google Sheet and Drive folder with the service account email (found in the JSON file as `client_email`)

**Get your Sheet ID**: From the URL `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`

**Get your Drive Folder ID**: Open the root folder in Drive, the ID is in the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

### YouTube Data API v3

1. In the same Google Cloud project, go to "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure OAuth consent screen:
   - Choose "External"
   - Fill in app name and your email
   - Add scope: `https://www.googleapis.com/auth/youtube.upload`
   - Add your email as a test user
4. Create OAuth Client ID:
   - Application type: "Desktop app"
   - Name it (e.g., "YouTube Uploader")
   - Download JSON
5. Copy the entire JSON content to GitHub secret `YOUTUBE_CLIENT_SECRETS`

**Note**: First run will require manual OAuth authorization. See [Manual Authorization](#manual-authorization) section.

### Instagram (using instagrapi)

Simply add your Instagram username and password as GitHub secrets:
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`

**Important**: 
- Use an Instagram Business or Creator account for best results
- Consider using a dedicated account or app-specific password
- Instagram may require 2FA verification on first login

### Manual Authorization

The first time the script runs, YouTube OAuth will need manual authorization:

1. Run locally once: `python main.py`
2. It will open a browser for you to authorize
3. After authorization, a `token.pickle` file is created
4. Upload this file as a GitHub secret named `YOUTUBE_TOKEN` (optional advanced setup)

Alternatively, use GitHub Actions with manual workflow trigger for first run.

## 🧪 Testing Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
GOOGLE_SHEETS_ID=your_sheet_id
DRIVE_FOLDER_ID=your_folder_id
GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
YOUTUBE_CLIENT_SECRETS='{"installed":{...}}'
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

3. Run:
```bash
python main.py
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

### YouTube upload fails
- Check daily quota (10,000 units/day, ~6 uploads)
- Verify OAuth token is valid
- Check video file size (max 128 GB for YouTube)

### Instagram upload fails
- Verify account is not restricted
- Check video meets requirements (max 60 seconds, MP4 format)
- Try using a business account
- Check for 2FA issues

## 📊 Character Limits

Auto-applied by the system:

- **YouTube Title**: 100 characters (truncated with "..." if longer)
- **YouTube Description**: 5,000 characters
- **Instagram Caption**: 2,200 characters (includes hashtags)

## 🎨 Cover Images

- Name cover files with `_cover` suffix (e.g., `video_cover.jpg`)
- Supported formats: JPG, PNG
- If no cover found, script auto-extracts frame at 1 second
- Used for both YouTube thumbnail and Instagram cover

## 📈 Phase 2 Features (Future)

- TikTok integration
- Spotify for Podcasters
- Auto-generated subtitles
- Analytics tracking
- Email/Slack notifications

## 🆘 Support

If you encounter issues:
1. Check GitHub Actions logs for error messages
2. Verify all secrets are set correctly
3. Test locally with `.env` file
4. Check API quotas and limits

## 📄 License

MIT License - feel free to modify and use for your own projects!

---

Built with ❤️ for automating content distribution

