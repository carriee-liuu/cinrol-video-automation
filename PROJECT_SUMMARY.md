# 🎉 Your Video Automation System is Ready!

## What Was Built

A complete automated video upload system that runs on GitHub Actions for **FREE** every Tuesday and Thursday at 11 AM.

## 📦 Files Created

### Core Application Files
- **`main.py`** - Main orchestrator that runs everything
- **`config.py`** - Configuration and credential management
- **`metadata_manager.py`** - Reads video info from Google Sheets
- **`google_drive_handler.py`** - Downloads videos from Drive
- **`youtube_uploader.py`** - Uploads to YouTube with thumbnails
- **`instagram_uploader.py`** - Uploads Reels to Instagram
- **`thumbnail_extractor.py`** - Extracts/optimizes video thumbnails

### Configuration Files
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Keeps secrets safe
- **`.github/workflows/upload_videos.yml`** - GitHub Actions scheduler

### Documentation
- **`README.md`** - Main documentation with API setup guide
- **`QUICKSTART.md`** - 30-minute fast setup guide ⚡
- **`SETUP_GUIDE.md`** - Comprehensive step-by-step guide
- **`SHEET_TEMPLATE.md`** - Google Sheet structure explained
- **`env_example.txt`** - Example environment variables for local testing

## 🎯 How It Works

### The Flow

1. **GitHub Actions triggers** every Tuesday/Thursday at 11 AM
2. **Script reads Google Sheet** to find today's video info
3. **Downloads from Drive**: 
   - Tuesday: Uses `reel_1/` folder
   - Thursday: Uses `reel_2/` folder (from Tuesday's row)
4. **Gets thumbnail**: Custom cover or auto-extracts from video
5. **Uploads to YouTube** with title, description, thumbnail
6. **Uploads to Instagram** with caption and cover
7. **Updates sheet** status columns automatically

### Key Features

✅ Fully automated - no manual intervention needed
✅ Free hosting on GitHub Actions
✅ Smart date handling (Thursday uses Tuesday's date)
✅ Custom cover images supported
✅ Auto-thumbnail extraction fallback
✅ Character limit validation
✅ Status tracking in sheet
✅ Retry logic for Instagram
✅ Error handling throughout

## 📋 What You Need to Do Next

### 1. Set Up Google Cloud (10 min)
- Create project
- Enable APIs (Drive, Sheets, YouTube)
- Create service account + download JSON
- Create YouTube OAuth + download JSON
- Share Sheet and Drive with service account email

### 2. Update Your Sheet (5 min)
- Add **Column J: "Folder Name"**
- Fill in exact folder names from Drive
- Example: `biggest moments of 2025`

### 3. Organize Google Drive (varies)
Structure your folders like this:
```
📁 [Your Root Folder]/
  └── 📁 biggest moments of 2025/
      └── 📁 biggest moments of 2025_reels/
          ├── 📁 reel_1/  ← Tuesday video
          │   ├── video.mp4
          │   └── video_cover.jpg
          └── 📁 reel_2/  ← Thursday video
              ├── video.mp4
              └── video_cover.jpg
```

### 4. Create GitHub Repo (5 min)
```bash
cd /Users/carrieliu/cursor-files
git init
git add .
git commit -m "Initial commit: Video automation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 5. Add GitHub Secrets (5 min)
Go to repo Settings → Secrets and variables → Actions

Add these 6 secrets:
1. `GOOGLE_SHEETS_ID`
2. `DRIVE_FOLDER_ID`
3. `GOOGLE_DRIVE_CREDENTIALS` (entire JSON)
4. `YOUTUBE_CLIENT_SECRETS` (entire JSON)
5. `INSTAGRAM_USERNAME`
6. `INSTAGRAM_PASSWORD`

### 6. Test Locally First (5 min)
```bash
pip install -r requirements.txt
# Create .env file with your credentials
python main.py
```

Authorize YouTube when browser opens (one-time setup).

### 7. Let It Run! 🚀
Once tested, the automation will run automatically every Tuesday and Thursday.

## 📖 Documentation Guide

Start here based on your preference:

- **Want to start NOW?** → Read `QUICKSTART.md`
- **Want step-by-step?** → Read `SETUP_GUIDE.md`
- **Need API help?** → See "API Setup Guide" in `README.md`
- **Sheet questions?** → Read `SHEET_TEMPLATE.md`
- **General reference?** → See `README.md`

## 🔑 Important URLs You'll Need

### Google Cloud
- Console: https://console.cloud.google.com/
- Enable APIs: https://console.cloud.google.com/apis/library

### Get Your IDs
- **Sheet ID**: From URL `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
- **Drive Folder ID**: From URL `https://drive.google.com/drive/folders/FOLDER_ID`

### Your Sheet
- Current sheet: https://docs.google.com/spreadsheets/d/11Oo5xYZo6rIqMSvsuFtULn9k-IjTOgm3LjymiFVa0Fo/edit

## 🎨 Customization Options

### Change Upload Time
Edit `.github/workflows/upload_videos.yml`:
```yaml
schedule:
  - cron: '0 15 * * 2,4'  # 15:00 UTC = 11 AM EST
```

### Change Privacy Settings
In `main.py`, find:
```python
privacy_status="public"
```
Change to `"private"` or `"unlisted"` if needed.

### Add More Platforms
Phase 2 features coming:
- TikTok integration
- Spotify for Podcasters
- Email notifications

## 💡 Tips for Success

1. **Always use Tuesday dates** in your sheet
2. **Test locally** before relying on automation
3. **Keep folder names exact** - case-sensitive!
4. **Check status columns** after each run
5. **Pre-upload 2-3 weeks** of content in advance
6. **Monitor first few runs** to ensure everything works

## 🆘 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "No video found" | Check sheet date and type="Podcast" |
| "Folder not found" | Verify folder structure and names match |
| "Permission denied" | Share resources with service account |
| "YouTube failed" | Complete OAuth authorization |
| "Instagram failed" | Check credentials and account type |

## 📊 Resource Usage

- **GitHub Actions**: ~5-10 minutes per run (2,000 free minutes/month)
- **Google APIs**: Well under free tier limits
- **YouTube API**: ~1,600 units per upload (10,000 daily limit = 6 videos/day)

## 🎬 Example Workflow

**Sunday Evening:**
1. Record podcast episode
2. Edit and export 2 short reels
3. Upload to Drive in correct folders
4. Add row to Google Sheet with Tuesday date

**Tuesday 11 AM:**
- ✅ Automation uploads `reel_1` to YouTube & Instagram
- ✅ Sheet updates with "UPLOADED" status

**Thursday 11 AM:**
- ✅ Automation uploads `reel_2` to YouTube & Instagram  
- ✅ Sheet updates with "UPLOADED" status

**You:** Relax! ☕

## 🚀 You're All Set!

Everything is built and ready to go. Just follow the setup steps and you'll have your automated video distribution system running!

**Questions?** Check the documentation files or test locally first.

**Ready to start?** Begin with `QUICKSTART.md`!

---

Built with ❤️ for CINROL

