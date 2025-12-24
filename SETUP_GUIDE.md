# Complete Setup Guide

Step-by-step guide to set up the CINROL Video Automation System.

## Prerequisites

- GitHub account
- Google Cloud account
- YouTube channel
- Instagram Business or Creator account
- Videos organized in Google Drive

## Part 1: Google Cloud Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "video-automation" (or your choice)
4. Click "Create"

### 2. Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - **Google Drive API**
   - **Google Sheets API**
   - **YouTube Data API v3**

### 3. Create Service Account (for Drive & Sheets)

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - Name: `video-automation-service`
   - Description: "Service account for video automation"
4. Click "Create and Continue"
5. Skip optional grant access steps
6. Click "Done"

### 4. Generate Service Account Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create" (downloads JSON file)
6. **Save this file securely** - you'll need it later

### 5. Share Google Resources with Service Account

1. Open the downloaded JSON file
2. Find the `client_email` field (e.g., `video-automation-service@project.iam.gserviceaccount.com`)
3. Share your Google Sheet with this email (Editor access)
4. Share your Google Drive folder with this email (Viewer access)

### 6. Create YouTube OAuth Credentials

1. Still in "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: "External"
   - App name: "CINROL Video Uploader"
   - User support email: Your email
   - Developer email: Your email
   - Click "Save and Continue"
   - Scopes: Click "Add or Remove Scopes"
     - Add: `https://www.googleapis.com/auth/youtube.upload`
   - Test users: Add your email
   - Click "Save and Continue"
4. Back to OAuth client creation:
   - Application type: "Desktop app"
   - Name: "YouTube Uploader"
   - Click "Create"
5. Download the JSON file
6. **Save this file securely**

## Part 2: Prepare Your Google Drive

### 1. Organize Folders

Structure your folders like this:

```
📁 CINROL Videos/  ← Root folder (share with service account)
  └── 📁 biggest moments of 2025/
      ├── raw files...
      └── 📁 biggest moments of 2025_reels/
          ├── 📁 reel_1/
          │   ├── video.mp4
          │   └── video_cover.jpg  (optional)
          └── 📁 reel_2/
              ├── video.mp4
              └── video_cover.jpg  (optional)
```

**Key Points:**
- Main folder can be any name (you'll need its ID)
- Each podcast episode has a folder
- Inside each podcast folder, create `[FOLDER_NAME]_reels/` folder
- Inside `_reels`, create `reel_1/` and `reel_2/` folders
- Put one video in each reel folder
- Cover images are optional, must end with `_cover`

### 2. Get Folder IDs

**Root Folder ID:**
1. Open your root folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the `FOLDER_ID_HERE` part

**Sheet ID:**
1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
3. Copy the `SHEET_ID_HERE` part

## Part 3: Update Your Google Sheet

### 1. Add Column J

Add a new column (J) with header: **"Folder Name"**

### 2. Fill in Folder Names

For each row (podcast episode), add the exact folder name from Google Drive.

Example:
- If your folder is `biggest moments of 2025`
- Put `biggest moments of 2025` in Column J

See [SHEET_TEMPLATE.md](SHEET_TEMPLATE.md) for full details.

## Part 4: GitHub Repository Setup

### 1. Create Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `cinrol-video-automation` (or your choice)
4. Choose Public or Private
5. Don't initialize with README (we have one)
6. Click "Create repository"

### 2. Push Code

```bash
cd /Users/carrieliu/cursor-files
git init
git add .
git commit -m "Initial commit: Video automation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 3. Add GitHub Secrets

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add each of these secrets:

**GOOGLE_SHEETS_ID**
- Value: The Sheet ID from Part 2, Step 2

**DRIVE_FOLDER_ID**
- Value: The Folder ID from Part 2, Step 2

**GOOGLE_DRIVE_CREDENTIALS**
- Open the service account JSON file
- Copy the ENTIRE contents (all of it, including `{` and `}`)
- Paste as the secret value

**YOUTUBE_CLIENT_SECRETS**
- Open the YouTube OAuth JSON file
- Copy the ENTIRE contents
- Paste as the secret value

**INSTAGRAM_USERNAME**
- Value: Your Instagram username

**INSTAGRAM_PASSWORD**
- Value: Your Instagram password

## Part 5: First-Time YouTube Authorization

YouTube requires OAuth authorization the first time. You have two options:

### Option A: Local Authorization (Recommended)

1. Install Python and dependencies:
```bash
cd /Users/carrieliu/cursor-files
pip install -r requirements.txt
```

2. Create `.env` file (copy from `env_example.txt` and fill in values)

3. Run script locally:
```bash
python main.py
```

4. A browser will open for you to authorize YouTube access
5. After authorization, a `youtube_token.pickle` file is created
6. This file can be uploaded to GitHub secrets for automated runs (advanced)

### Option B: GitHub Actions Manual Run

1. Go to repository → "Actions" tab
2. Click "Upload Videos to Social Media" workflow
3. Click "Run workflow" → "Run workflow"
4. The workflow will fail on first run (expected)
5. You'll need to authorize via local method eventually

## Part 6: Test the System

### 1. Local Testing

```bash
cd /Users/carrieliu/cursor-files
python main.py
```

Watch for:
- ✓ Configuration loaded
- ✓ Connected to Google Sheets
- ✓ Found video metadata
- ✓ Downloaded video
- ✓ YouTube upload successful
- ✓ Instagram upload successful

### 2. Check Results

- Open your Google Sheet - status columns should update
- Check YouTube - video should appear
- Check Instagram - reel should appear

## Part 7: Schedule Automation

The GitHub Actions workflow is already configured to run:
- **Every Tuesday at 11:00 AM EST** (15:00 UTC)
- **Every Thursday at 11:00 AM EST** (15:00 UTC)

### Adjust Timezone (if needed)

Edit `.github/workflows/upload_videos.yml`:

```yaml
schedule:
  - cron: '0 15 * * 2,4'  # 15:00 UTC
```

**Time conversions:**
- 11 AM EST = 15:00 UTC (16:00 UTC during DST)
- 11 AM PST = 19:00 UTC (18:00 UTC during DST)
- 11 AM CST = 17:00 UTC (16:00 UTC during DST)

## Troubleshooting

### "No video found for today's date"
- Check Google Sheet has correct date in Column C
- Verify Column B says "Podcast"
- Make sure Column J has folder name

### "Could not find folder"
- Verify folder structure matches exactly
- Check folder name in Column J matches Drive
- Ensure service account has access to Drive folder

### "YouTube upload failed"
- Complete OAuth authorization (Part 5)
- Check API quotas (10,000 units/day)
- Verify video format (MP4 recommended)

### "Instagram upload failed"
- Check username/password are correct
- Verify account is Business/Creator type
- May need to handle 2FA manually first time

### "Permission denied" errors
- Check service account has access to Sheet
- Check service account has access to Drive folder
- Verify all GitHub secrets are set correctly

## Maintenance

### Weekly Checklist
- [ ] Add upcoming podcast episodes to sheet
- [ ] Upload videos to Google Drive in correct folders
- [ ] Verify folder names match in sheet Column J
- [ ] Check previous uploads succeeded (status columns)

### Monthly Checklist
- [ ] Review GitHub Actions logs
- [ ] Check API quotas usage
- [ ] Update credentials if expired
- [ ] Clean up old temp files (automatic)

## Support

If you need help:
1. Check the main [README.md](README.md)
2. Review [SHEET_TEMPLATE.md](SHEET_TEMPLATE.md)
3. Look at GitHub Actions logs for errors
4. Test locally first before debugging automation

## Next Steps

Once everything is working:
1. Set up remaining weeks in your sheet
2. Upload all upcoming videos to Drive
3. Let the automation run automatically
4. Monitor the first few runs to ensure success

## Phase 2 Features (Coming Soon)

- TikTok integration
- Spotify for Podcasters
- Email/Slack notifications
- Auto-generated subtitles
- Enhanced error recovery

