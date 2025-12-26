# Troubleshooting Guide

## YouTube Publishing Issues

### Problem: "GitHub Actions publish didn't work at 11am"

**Root Cause:** GitHub Actions has a 6-hour maximum runtime. If you trigger a workflow that needs to wait more than ~5.8 hours, it will fail.

**Solution:** 
- Trigger the workflow **within 5.8 hours** of the publish time
- For 11 AM publishes, trigger between 5:30 AM - 10:59 AM

**Current Setup for Friday:**
```bash
# Option 1: Automatic (Mac must be on at 5:30 AM)
- Cron job runs at 5:30 AM EST on Friday
- Triggers GitHub Actions
- GitHub Actions waits and publishes at 11:00 AM

# Option 2: Manual (you run it Friday morning)
./trigger_friday_publish.sh
# Run this anytime between 5:30-10:59 AM EST on Friday
```

### Problem: "Request had insufficient authentication scopes"

**Root Cause:** The YouTube token was created with `youtube.upload` scope, but changing video privacy requires `youtube.force-ssl` scope.

**Solution:**
1. Delete old token: `rm temp/youtube_token.pickle`
2. Run any YouTube script to trigger re-authorization
3. Authorize in browser
4. Update GitHub secret:
   ```bash
   base64 -i temp/youtube_token.pickle | gh secret set YOUTUBE_TOKEN_BASE64
   ```

**Fixed:** ✅ We updated `youtube_uploader.py` to use `youtube.force-ssl` scope

## Instagram Publishing Issues

### Problem: Instagram doesn't support scheduling via API

**Current Solution:** Local cron job
- Mac must be ON at scheduled time
- Uploads happen immediately when cron triggers

**Alternative:** Use Meta Business Suite UI for manual scheduling

## General Debugging

### View Scheduled Cron Jobs
```bash
crontab -l
```

### View GitHub Actions Status
```bash
gh run list --workflow=publish_video.yml --limit 5
```

### View Specific Run Logs
```bash
gh run view RUN_ID --log
```

### Test YouTube Publishing Locally
```bash
python3 publish_video.py VIDEO_ID
```

### Manual Upload
```bash
python3 manual_upload.py \
  --folder "GOOGLE_DRIVE_FOLDER_URL" \
  --title "Video Title" \
  --description "Description" \
  --platform youtube
```

## Common Errors

### Video uploads to wrong YouTube account
**Solution:** Re-authorize
```bash
rm temp/youtube_token.pickle
python3 publish_video.py VIDEO_ID
# Authorize with correct account in browser
```

### Instagram: "Login required" error
**Solution:** Update credentials in `.env`
```bash
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Google Drive: "File not found"
**Solution:** Check folder permissions
1. Right-click folder → Share → Anyone with link can view
2. Verify folder contains video file and _cover file

## Best Practices

### For Scheduled YouTube Shorts:
1. Upload as PRIVATE first
2. Schedule publication using GitHub Actions (within 5.8 hours)
3. Your Mac can be OFF during publication if you triggered GitHub Actions

### For Scheduled Instagram:
1. Mac MUST be ON at publish time
2. Prevent sleep: System Settings → Lock Screen → Never
3. Keep terminal open if testing

### For Manual Uploads:
1. Always test with `--privacy private` first
2. Verify video appears correctly
3. Then publish or schedule for public

## Contact & Support

If issues persist:
1. Check GitHub Actions logs
2. Check local logs: `cat logs/*.log`
3. Verify all credentials are up to date
4. Ensure all cron jobs are properly formatted: `crontab -l`

