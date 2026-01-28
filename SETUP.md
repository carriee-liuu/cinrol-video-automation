# Setup Guide

Quick reference for setting up the CINROL Video Automation System.

## Prerequisites

- Python 3.10+ installed
- Mac computer (for cron scheduling)
- Google account with Drive and Sheets access
- YouTube channel
- Instagram account (Business/Creator recommended)

## Step-by-Step Setup

### 1. Clone and Install

```bash
git clone https://github.com/carriee-liuu/cinrol-video-automation.git
cd cinrol-video-automation
pip3 install -r requirements.txt
```

### 2. Set Up Google APIs

#### Google Drive & Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project → Enable Google Drive API and Google Sheets API
3. Create Service Account:
   - Credentials → Create Credentials → Service Account
   - Name: "video-automation"
   - Create and Continue → Skip optional steps
4. Generate JSON key:
   - Click service account → Keys tab → Add Key → Create new key → JSON
   - Download the JSON file
5. Share resources:
   - Copy the `client_email` from JSON
   - Share your Google Sheet with this email (Editor access)
   - Share your Drive root folder with this email (Viewer access)

#### YouTube Data API v3

1. In same Google Cloud project:
   - Credentials → Create Credentials → OAuth 2.0 Client ID
2. Configure OAuth consent screen:
   - External → App name, email
   - Scopes: `https://www.googleapis.com/auth/youtube.force-ssl`
   - Add your email as test user
3. Create OAuth Client:
   - Application type: Desktop app
   - Name: "YouTube Uploader"
   - Download JSON

### 3. Configure Environment Variables

Create `.env` file:

```bash
cp env_example.txt .env
```

Edit `.env` with your values:

```bash
GOOGLE_SHEETS_ID=your_sheet_id_from_url
DRIVE_FOLDER_ID=your_root_folder_id_from_url
GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'  # Entire JSON
YOUTUBE_CLIENT_SECRETS='{"installed":{...}}'  # Entire JSON
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### 4. Set Up Google Sheet

Add these columns to your sheet:

| Column | Header | Example |
|--------|--------|---------|
| A | what (CINROLLING) | biggest moments of 2025 |
| B | type | Podcast |
| C | planned publish date | 12/23/2025 |
| J | Folder Name | biggest moments of 2025 |
| G | long-form description | Full description... |
| H | short-form description | Short caption... |

### 5. Organize Google Drive

Create this structure:

```
Root Folder (ID in DRIVE_FOLDER_ID)
└── Folder Name (from Column J)
    └── Folder Name_reels
        ├── reel_1/  (Tuesday)
        │   ├── video.mp4
        │   └── video_cover.jpg  (optional)
        └── reel_2/  (Thursday)
            ├── video.mp4
            └── video_cover.jpg  (optional)
```

### 6. Set Up Cron Job (Scheduled Uploads)

The cron job is already configured. Verify:

```bash
crontab -l
```

Should show:
```
0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

If not present, add it:
```bash
crontab -e
# Add this line:
0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

### 7. Test Setup

```bash
# Test manual upload
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" \
  --title "Test" \
  --description "Test" \
  --caption "Test #test" \
  --platform all

# Test scheduled upload (reads from sheet)
python3 main.py
```

### 8. First YouTube Authorization

On first run, YouTube will require OAuth authorization:
1. Script opens browser automatically
2. Sign in with your YouTube account
3. Authorize the app
4. `temp/youtube_token.pickle` is created (don't commit to git)

## Verification Checklist

- [ ] Python dependencies installed
- [ ] `.env` file created with all credentials
- [ ] Google Sheet has required columns
- [ ] Google Drive folder structure matches expected format
- [ ] Service account has access to Sheet and Drive
- [ ] Cron job is set up (for scheduled uploads)
- [ ] Test manual upload works
- [ ] Test scheduled upload works
- [ ] Mac sleep settings configured (for cron)

## Next Steps

- See `README.md` for detailed usage
- See `MANUAL_UPLOAD_GUIDE.md` for manual upload examples
- See `LOCAL_SCHEDULING_GUIDE.md` for cron scheduling details
- See `TROUBLESHOOTING.md` for common issues
