# Automated Video Upload System - Setup Complete! 🎉

## What's Been Set Up

Your video automation system is now configured to run **automatically** every **Tuesday and Thursday at 11:00 AM EST**.

## How It Works

1. **Cron Job** runs at 11 AM EST on Tuesdays and Thursdays
2. Script looks up today's video info from your Google Sheet
3. Downloads video and cover from Google Drive
4. Uploads to **YouTube** (immediately, since Shorts can't be scheduled via API)
5. Uploads to **Instagram Reels** with caption and cover
6. Updates Instagram bio links (only on Tuesdays)
7. Logs everything to `logs/automation_YYYYMMDD_HHMMSS.log`

## Important Notes

### ✅ What's Automated
- Video downloads from Google Drive
- YouTube uploads
- Instagram Reels uploads
- Instagram bio updates
- Thumbnail handling

### ⚠️ Requirements
- **Your Mac must be ON and AWAKE** at 11 AM EST on Tuesdays/Thursdays
- Internet connection required
- Google Sheet must be updated with video metadata

### 📋 Google Sheet Requirements

Your sheet needs these columns filled in for automation to work:

| Column | Name | Required | Example |
|--------|------|----------|---------|
| C | Planned Publish Date | ✅ | 12/24/24 (Tuesday or Thursday) |
| B | Type | ✅ | Podcast |
| J | Folder Name | ✅ | episode_42 |
| G | Long-form Description | ✅ | Full podcast episode description |
| H | Short-form Description | ✅ | Short caption for Reels |
| K | Episode Number | For Tuesday only | 42 |
| L | Spotify URL | For Tuesday only | https://... |
| M | YouTube URL | For Tuesday only | https://... |

### 📁 Google Drive Folder Structure

Your videos should be organized like this:
```
[Root Folder: 1-PFvV4cEmnlVXA78dwjgxhDkYoMv5cZL]
└── episode_42/
    └── episode_42_reels/
        ├── reel_1/           ← Tuesday video
        │   ├── video.mp4
        │   └── video_cover.jpg (optional)
        └── reel_2/           ← Thursday video
            ├── video.mp4
            └── video_cover.jpg (optional)
```

## Manual Upload Script (Still Available!)

You can still manually upload videos anytime using:

```bash
cd /Users/carrieliu/cinrol-video-automation

python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" \
  --title "Your Video Title" \
  --description "Your description" \
  --platform youtube

# Or for both platforms:
python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" \
  --title "Your Video Title" \
  --description "Your description" \
  --caption "Instagram caption with #hashtags" \
  --platform both
```

**Note:** Scheduling doesn't work for YouTube Shorts. Videos post immediately.

## Checking Logs

View automation logs:
```bash
cd /Users/carrieliu/cinrol-video-automation
ls -lt logs/
cat logs/automation_YYYYMMDD_HHMMSS.log
```

## Testing the Automation

Test the automation script without waiting for Tuesday/Thursday:

```bash
cd /Users/carrieliu/cinrol-video-automation
./run_automation.sh
```

This will:
- Look for today's video in your Google Sheet
- Download and upload if found
- Create a log file in the `logs/` directory

## Managing the Cron Job

### View Current Cron Jobs
```bash
crontab -l
```

### Edit Cron Jobs
```bash
crontab -e
```

### Disable Automation (Temporarily)
```bash
# Comment out the line by adding # at the beginning
crontab -e
# Change:  0 11 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
# To:      # 0 11 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

### Re-enable Automation
```bash
# Remove the # from the beginning of the line
crontab -e
```

### Remove Automation Completely
```bash
crontab -r
```

## Troubleshooting

### Issue: Videos aren't uploading
1. Check logs: `cat logs/automation_*.log | tail -100`
2. Verify your Mac was awake at 11 AM
3. Test manually: `./run_automation.sh`
4. Check Google Sheet has correct date and data

### Issue: Instagram login failed
- Instagram may require re-authentication
- Run the manual script once to re-login
- Instagram blocks suspicious activity - may need to verify account

### Issue: "No video found for today's date"
- Check Google Sheet has a row with today's date (Column C)
- For Thursday, ensure Tuesday's date is in the sheet (script looks back 2 days)
- Type column (B) must be "Podcast"
- Folder Name column (J) must be filled

### Issue: Video downloaded but upload failed
- Check API credentials in `.env` file
- YouTube: May need to re-authorize (run manual script once)
- Instagram: May need to login again

## Important Reminders

1. **Keep your Mac awake** at 11 AM on Tuesdays and Thursdays
2. **Update Google Sheet** before each upload with video metadata
3. **Check logs** after each run to ensure success
4. **Manual script** is always available as backup

## Support

For issues or questions, check:
- Logs directory: `/Users/carrieliu/cinrol-video-automation/logs/`
- Configuration: `/Users/carrieliu/cinrol-video-automation/.env`
- Google Sheet: https://docs.google.com/spreadsheets/d/11Oo5xYZo6rIqMSvsuFtULn9k-IjTOgm3LjymiFVa0Fo

---

**You're all set! 🚀**

Next upload: Check `crontab -l` to see schedule

