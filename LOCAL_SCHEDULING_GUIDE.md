# Local Scheduling Guide

## Overview

All video scheduling now uses **local cron jobs** on your Mac. This means:

✅ **Advantages:**
- Schedule weeks/months in advance (no 6-hour limit)
- Simpler setup (no GitHub Actions complexity)
- Full control over timing

⚠️ **Requirements:**
- Your Mac must be ON and AWAKE at scheduled time
- Prevent sleep: System Settings → Lock Screen → Turn display off: Never

---

## Quick Reference

### Schedule YouTube Short + Instagram Post

For the same video on both platforms:

```bash
# 1. Schedule YouTube (uploads as private, publishes at scheduled time)
./schedule_youtube_local.sh \
  "GOOGLE_DRIVE_FOLDER_LINK" \
  "Video Title" \
  "Video description #hashtags" \
  "2024-12-27 11:00"

# 2. Schedule Instagram (uploads at scheduled time)
./schedule_upload.sh \
  "GOOGLE_DRIVE_FOLDER_LINK" \
  "Caption with #hashtags" \
  "Short description" \
  "11:00" \
  "instagram"
```

### Schedule Individual Platforms

**YouTube only:**
```bash
./schedule_youtube_local.sh \
  "https://drive.google.com/drive/folders/FOLDER_ID" \
  "My Video Title" \
  "Description text #hashtags" \
  "2024-12-30 14:00"
```

**Instagram only:**
```bash
./schedule_upload.sh \
  "https://drive.google.com/drive/folders/FOLDER_ID" \
  "Caption with #hashtags" \
  "Description" \
  "14:00" \
  "instagram"
```

**TikTok only:**
```bash
./schedule_upload.sh \
  "https://drive.google.com/drive/folders/FOLDER_ID" \
  "Caption with #hashtags" \
  "Description" \
  "14:00" \
  "tiktok"
```

---

## How It Works

### YouTube Scheduling (2-step process):

1. **Upload as PRIVATE** (happens immediately)
   - Video is uploaded to YouTube
   - Set to PRIVATE so nobody can see it
   - You get the video ID and URL

2. **Schedule Publication** (happens at your specified time)
   - Cron job runs at scheduled time
   - Changes video from PRIVATE → PUBLIC
   - Mac must be ON at this time

### Instagram/TikTok Scheduling (1-step process):

1. **Schedule Upload** (happens at your specified time)
   - Cron job runs at scheduled time
   - Uploads video directly
   - Mac must be ON at this time

---

## Managing Scheduled Jobs

### View All Scheduled Jobs
```bash
crontab -l
```

### Edit Scheduled Jobs Manually
```bash
crontab -e
```

### Remove All Scheduled Jobs (CAREFUL!)
```bash
crontab -r
```

### Remove Specific Job
```bash
# 1. List jobs and find the one to remove
crontab -l

# 2. Edit and delete that line
crontab -e
# Delete the line, save and quit (:wq in vim)
```

---

## Cron Job Format

```
MINUTE HOUR DAY MONTH DAYOFWEEK COMMAND
```

Examples:
```bash
# Every Tuesday and Thursday at 11 AM
0 11 * * 2,4 /path/to/script.sh

# Specific date: Dec 27 at 11 AM
0 11 27 12 * /path/to/script.sh

# Every day at 2:30 PM
30 14 * * * /path/to/script.sh

# First day of every month at 9 AM
0 9 1 * * /path/to/script.sh
```

---

## Troubleshooting

### Mac went to sleep during scheduled time
**Problem:** Video didn't post because Mac was asleep  
**Solution:** 
1. System Settings → Lock Screen
2. Set "Turn display off on battery when inactive" to Never
3. Set "Turn display off on power adapter when inactive" to Never

### Cron job didn't run
**Check logs:**
```bash
# View specific log file
cat logs/youtube_dec27.log
cat logs/instagram_dec27.log

# View all recent logs
ls -lt logs/
```

### Video uploaded to wrong account
**Solution:** Re-authorize with correct account
```bash
# For YouTube:
rm temp/youtube_token.pickle
python3 publish_video.py VIDEO_ID
# Authorize in browser with correct account

# For Instagram:
# Update .env file with correct credentials
```

### Want to cancel a scheduled post
```bash
# 1. Find the video ID or job line
crontab -l | grep "VIDEO_ID_OR_FOLDER"

# 2. Remove that line
crontab -e
# Delete the line, save (:wq)
```

---

## Examples from Your Setup

### Friday Dec 27 Schedule
```bash
# Current setup (both at 11 AM):

# Instagram upload
0 11 27 12 * cd /Users/carrieliu/cinrol-video-automation && \
  python3 manual_upload.py \
  --folder "https://drive.google.com/drive/folders/15uEEp7jNzxmiRqu_1CwwHZQPcc9BE9f9" \
  --caption "culinarily speaking whats the difference between creme brule and caramel mousse..." \
  --platform instagram >> logs/instagram_dec27.log 2>&1

# YouTube publish (video already uploaded as private: oTwZlvK-B28)
0 11 27 12 * cd /Users/carrieliu/cinrol-video-automation && \
  python3 publish_video.py oTwZlvK-B28 >> logs/youtube_dec27.log 2>&1
```

### Recurring Tuesday/Thursday Posts
```bash
# Automated Google Sheet workflow
0 11 * * 2,4 /Users/carrieliu/cinrol-video-automation/run_automation.sh
```

---

## Best Practices

### 1. Always test first
```bash
# Test YouTube upload as private first
python3 manual_upload.py \
  --folder "FOLDER_LINK" \
  --title "Test" \
  --description "Test" \
  --privacy private \
  --platform youtube
```

### 2. Keep your Mac awake
- Use Amphetamine or Caffeine app
- Or: System Settings → Energy Saver → Prevent sleep

### 3. Check logs after scheduled posts
```bash
tail -20 logs/youtube_dec27.log
tail -20 logs/instagram_dec27.log
```

### 4. Schedule with buffer time
If posting at 11 AM, set cron for 11:00, not 11:01
Cron jobs are precise to the minute

### 5. Clean up old cron jobs
After videos post, remove their cron entries:
```bash
crontab -e
# Delete lines for past dates
```

---

## GitHub Actions (REMOVED)

**Why we removed it:**
- 6-hour maximum runtime limit
- Can't schedule weeks in advance
- More complex than local cron
- Requires Mac to be on to trigger anyway

**Local cron is simpler and more flexible for your use case!**

---

## Quick Commands Cheat Sheet

```bash
# View scheduled jobs
crontab -l

# Schedule YouTube Short for specific date/time
./schedule_youtube_local.sh "FOLDER" "TITLE" "DESC" "YYYY-MM-DD HH:MM"

# Schedule Instagram for specific time today
./schedule_upload.sh "FOLDER" "CAPTION" "DESC" "HH:MM" "instagram"

# Manually publish a private YouTube video now
python3 publish_video.py VIDEO_ID

# View logs
ls -lt logs/

# Test upload without scheduling
python3 manual_upload.py --folder "LINK" --title "TITLE" --description "DESC" --platform youtube
```

