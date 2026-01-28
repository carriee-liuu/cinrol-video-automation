# Setup Guide

Complete setup instructions for the CINROL Video Automation System, including setup in Cursor or Claude Code with AI assistance.

## Prerequisites

- Python 3.10+ installed
- Mac computer (for cron scheduling)
- Google account with Drive and Sheets access
- YouTube channel
- Instagram account (Business/Creator recommended)
- **Cursor** or **Claude Code** (AI coding assistants) - recommended for workflow

## 🚀 Quick Setup in Cursor or Claude Code

### Why Use Cursor/Claude Code?

These AI coding assistants help you:
- Generate captions and hashtags
- Create upload commands
- Troubleshoot issues
- Understand the codebase
- Iterate on content quickly

### Step 1: Open Project in Cursor/Claude Code

1. **Clone the repository:**
   ```bash
   git clone https://github.com/carriee-liuu/cinrol-video-automation.git
   cd cinrol-video-automation
   ```

2. **Open in Cursor:**
   - File → Open Folder → Select `cinrol-video-automation`
   - Or: `cursor cinrol-video-automation`

3. **Open in Claude Code:**
   - File → Open Folder → Select `cinrol-video-automation`
   - Or: `claude cinrol-video-automation`

### Step 2: Set Up Environment

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Create `.env` file:**
   - Copy `env_example.txt` to `.env`
   - Or ask AI: "Help me create a .env file based on env_example.txt"

3. **Configure environment variables** (see Step 3 below)

### Step 3: Configure Environment Variables

**Using AI Assistant:**

Ask Cursor/Claude Code:
```
Help me set up the .env file. I need to configure:
- Google Sheets ID
- Google Drive folder ID
- Google service account credentials
- YouTube OAuth credentials
- Instagram credentials

Guide me through getting each one.
```

**Manual Setup:**

Create `.env` file in project root:

```bash
GOOGLE_SHEETS_ID=your_sheet_id_from_url
DRIVE_FOLDER_ID=your_root_folder_id_from_url
GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'  # Entire JSON
YOUTUBE_CLIENT_SECRETS='{"installed":{...}}'  # Entire JSON
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

**Get your IDs:**

- **Google Sheet ID**: From URL `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
- **Drive Folder ID**: From URL `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

## 📋 Detailed Setup Steps

### Step 1: Clone and Install

```bash
git clone https://github.com/carriee-liuu/cinrol-video-automation.git
cd cinrol-video-automation
pip3 install -r requirements.txt
```

### Step 2: Set Up Google APIs

#### Google Drive & Sheets API

**Using AI Assistant:**
```
Walk me through setting up Google Drive and Sheets API:
1. Creating a project
2. Enabling APIs
3. Creating a service account
4. Getting credentials
```

**Manual Steps:**

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
6. Copy entire JSON content to `.env` as `GOOGLE_DRIVE_CREDENTIALS`

#### YouTube Data API v3

**Using AI Assistant:**
```
Help me set up YouTube Data API v3 for uploading videos.
I need OAuth 2.0 credentials.
```

**Manual Steps:**

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
4. Copy entire JSON content to `.env` as `YOUTUBE_CLIENT_SECRETS`

### Step 3: Configure Environment Variables

**Using AI Assistant:**
```
I have my Google Cloud credentials. Help me format them correctly 
for the .env file. Show me the exact format for:
- GOOGLE_DRIVE_CREDENTIALS (service account JSON)
- YOUTUBE_CLIENT_SECRETS (OAuth JSON)
```

Create `.env` file:

```bash
cp env_example.txt .env
```

Edit `.env` with your values (see `env_example.txt` for format).

### Step 4: Set Up Google Sheet

**Using AI Assistant:**
```
Help me set up my Google Sheet for video automation. What columns 
do I need and what should they contain?
```

**Required Columns:**

| Column | Header | Example |
|--------|--------|---------|
| A | what (CINROLLING) | biggest moments of 2025 |
| B | type | Podcast |
| C | planned publish date | 12/23/2025 |
| J | Folder Name | biggest moments of 2025 |
| G | long-form description | Full description... |
| H | short-form description | Short caption... |

**Important:**
- Column B must be exactly "Podcast" (case-sensitive)
- Column C dates must be in M/D/YYYY format
- Column J must match your Google Drive folder name exactly
- Only add rows for Tuesday dates (script uses same row for Thursday)

### Step 5: Organize Google Drive

**Using AI Assistant:**
```
Help me understand the Google Drive folder structure needed for 
video automation. Show me examples.
```

**Structure:**

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

**Cover Images:**
- Name files with `cover` or `thumbnail` in filename
- Supported: JPG, PNG, WEBP
- If not found, script extracts frame from video

### Step 6: Set Up Cron Job (Scheduled Uploads)

**Using AI Assistant:**
```
Help me set up a cron job to run the automation script every 
Tuesday and Thursday at 11 AM EST.
```

**Verify/Set Cron:**

```bash
# View current cron jobs
crontab -l

# Should show:
0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

**If not present, add it:**
```bash
crontab -e
# Add this line (adjust path to your location):
0 8 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

**Important:**
- Cron runs at 8 AM PST = 11 AM EST
- Mac must be ON and AWAKE at scheduled time
- Configure Mac sleep settings: System Settings → Lock Screen → Turn display off: Never

### Step 7: Test Setup

**Using AI Assistant:**
```
Help me test the video automation setup. What should I test first?
```

**Test Manual Upload:**

```bash
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" \
  --title "Test" \
  --description "Test description" \
  --caption "Test caption #test" \
  --platform all
```

**Test Scheduled Upload:**

```bash
python3 main.py
```

**Expected Output:**
- Connects to Google Sheets
- Downloads video from Drive
- Uploads to YouTube and Instagram
- Updates sheet status

### Step 8: First YouTube Authorization

**Using AI Assistant:**
```
I'm running the script for the first time. What should I expect 
for YouTube OAuth authorization?
```

**On first run:**
1. Script opens browser automatically
2. Sign in with your YouTube account
3. Authorize the app
4. `temp/youtube_token.pickle` is created (don't commit to git)

## 🤖 Using AI Assistants for Workflow

### Getting Help with Captions

**In Cursor/Claude Code:**

```
I have a video about [topic]. Help me create:
1. An Instagram caption with hashtags
2. A YouTube title
3. A YouTube description

Context: [describe your video]
```

**Refine:**
```
Make the caption more casual
Add more trending hashtags
Give me a condensed version under 100 characters
```

### Creating Upload Commands

**Ask AI:**
```
Help me create the command to upload this video:
- Folder link: [paste Google Drive link]
- Title: [your title]
- Description: [your description]
- Caption: [your caption]
```

### Troubleshooting

**Ask AI:**
```
I'm getting this error: [paste error]
Help me troubleshoot and fix it.
```

**Common issues:**
- "Module not found" → Ask: "Help me install missing dependencies"
- "Authentication failed" → Ask: "Help me check my .env file"
- "Video not found" → Ask: "Help me verify my Google Drive folder structure"

## ✅ Verification Checklist

- [ ] Python dependencies installed (`pip3 install -r requirements.txt`)
- [ ] `.env` file created with all credentials
- [ ] Google Sheet has required columns (A, B, C, G, H, J)
- [ ] Google Drive folder structure matches expected format
- [ ] Service account has access to Sheet (Editor) and Drive (Viewer)
- [ ] Cron job is set up (for scheduled uploads)
- [ ] Test manual upload works
- [ ] Test scheduled upload works
- [ ] Mac sleep settings configured (for cron)
- [ ] YouTube OAuth authorized (first run)

## 📚 Next Steps

- **Read `WORKFLOW_GUIDE.md`** - Complete workflow for creating and posting content
- **Read `README.md`** - Detailed usage and features
- **Read `MANUAL_UPLOAD_GUIDE.md`** - Manual upload examples
- **Read `LOCAL_SCHEDULING_GUIDE.md`** - Cron scheduling details
- **Read `TROUBLESHOOTING.md`** - Common issues and solutions

## 💡 Pro Tips

1. **Use AI for everything:**
   - Caption generation
   - Command creation
   - Troubleshooting
   - Understanding code

2. **Save common prompts:**
   - Create a file with your favorite AI prompts
   - Reuse them for consistent results

3. **Iterate with AI:**
   - Don't accept first draft
   - Ask for revisions and variations
   - Get multiple options

4. **Test before posting:**
   - Always test with a small video first
   - Verify captions and metadata
   - Check uploads before scheduling

## 🆘 Getting Help

**Using AI Assistant:**
```
I need help with [specific issue]. Here's what I've tried:
[describe your attempts]

What should I do next?
```

**Check Documentation:**
- `README.md` - Main documentation
- `WORKFLOW_GUIDE.md` - Complete workflow
- `TROUBLESHOOTING.md` - Common issues

**Check Logs:**
```bash
# View recent logs
ls -lt logs/
tail -20 logs/automation_*.log
```

---

**Remember:** The AI assistant is your partner. Use it to understand, configure, and optimize your workflow!
