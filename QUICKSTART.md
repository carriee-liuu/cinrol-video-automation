# Quick Start Guide

Get your video automation running in 30 minutes!

## ⚡ Fast Track Setup

### Step 1: Get Your IDs (5 minutes)

1. **Google Sheet ID**: 
   - Open your sheet: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
   - Copy the ID from the URL
   
2. **Google Drive Folder ID**:
   - Open your root folder: `https://drive.google.com/drive/folders/YOUR_FOLDER_ID`
   - Copy the ID from the URL

### Step 2: Set Up Google Cloud (10 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "video-automation"
3. Enable APIs:
   - Google Drive API
   - Google Sheets API  
   - YouTube Data API v3
4. Create Service Account:
   - APIs & Services → Credentials → Create Credentials → Service Account
   - Download JSON key file
5. Create YouTube OAuth:
   - OAuth 2.0 Client ID → Desktop app
   - Download JSON key file

### Step 3: Share Access

1. Open your service account JSON file
2. Find `client_email` 
3. Share your Google Sheet with this email (Editor)
4. Share your Drive folder with this email (Viewer)

### Step 4: Update Your Sheet

Add **Column J: "Folder Name"** with your exact folder names from Drive.

Example row:
```
A: biggest moments of 2025
B: Podcast
C: 12/23/2025
...
J: biggest moments of 2025
```

### Step 5: Organize Drive Folders

Structure:
```
📁 Your Root Folder/
  └── 📁 biggest moments of 2025/
      └── 📁 biggest moments of 2025_reels/
          ├── 📁 reel_1/
          │   └── video.mp4
          └── 📁 reel_2/
              └── video.mp4
```

### Step 6: Create GitHub Repo (5 minutes)

1. Create new repo on GitHub
2. Push code:
```bash
cd /Users/carrieliu/cursor-files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 7: Add GitHub Secrets (5 minutes)

Go to Settings → Secrets and variables → Actions

Add these 6 secrets:
- `GOOGLE_SHEETS_ID` - Your sheet ID
- `DRIVE_FOLDER_ID` - Your folder ID
- `GOOGLE_DRIVE_CREDENTIALS` - Entire service account JSON
- `YOUTUBE_CLIENT_SECRETS` - Entire OAuth JSON
- `INSTAGRAM_USERNAME` - Your Instagram username
- `INSTAGRAM_PASSWORD` - Your Instagram password

### Step 8: Test Locally (5 minutes)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file (copy from `env_example.txt`)

3. Run:
```bash
python main.py
```

4. Authorize YouTube when browser opens

### Step 9: Done! 🎉

Your automation is now set up and will run:
- Every Tuesday at 11 AM
- Every Thursday at 11 AM

## 🔍 Quick Checks

✅ Service account has access to Sheet and Drive
✅ Column J added to sheet with folder names  
✅ Folders structured correctly: `[name]_reels/reel_1/` and `reel_2/`
✅ All 6 GitHub secrets added
✅ YouTube authorized (token created)
✅ Instagram credentials valid

## 📝 Weekly Workflow

1. Record and edit your podcast
2. Export 2 short reels
3. Upload to Drive: `[name]_reels/reel_1/` and `reel_2/`
4. Add row to sheet with Tuesday date
5. Automation handles the rest!

## 🆘 Having Issues?

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

Common fixes:
- **"No video found"** → Check sheet date and folder name
- **"Permission denied"** → Share resources with service account
- **"YouTube failed"** → Complete OAuth authorization
- **"Folder not found"** → Verify folder structure and naming

## ⏭️ Next Steps

1. Set up next 4 weeks of content in your sheet
2. Upload all videos to Drive
3. Monitor first automated run on Tuesday
4. Relax and let the system work! ☕

