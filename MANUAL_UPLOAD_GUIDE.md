# Manual Upload Guide

Quick reference for using `manual_upload.py` to upload videos on-demand.

## Setup (One Time)

1. Make sure you have credentials set up locally:
```bash
cd /Users/carrieliu/cinrol-video-automation
# Create .env file with your credentials (copy from env_example.txt)
pip install -r requirements.txt
```

2. Test the script:
```bash
python manual_upload.py --help
```

## Usage Examples

### Upload to Instagram Only

```bash
python manual_upload.py \
  --video "drive://biggest moments of 2025_reels/reel_1/video.mp4" \
  --caption "New episode out now! 🎙️ #cinrolling #podcast" \
  --platform instagram
```

With custom thumbnail:
```bash
python manual_upload.py \
  --video "drive://biggest moments of 2025_reels/reel_1/video.mp4" \
  --thumbnail "drive://biggest moments of 2025_reels/reel_1/video_cover.jpg" \
  --caption "New episode out now! 🎙️" \
  --platform instagram
```

### Upload to YouTube Only

```bash
python manual_upload.py \
  --video "drive://biggest moments of 2025_reels/reel_1/video.mp4" \
  --title "S1 E4: Biggest Moments of 2025" \
  --description "Join us as we look back on 2025..." \
  --thumbnail "drive://biggest moments of 2025_reels/reel_1/video_cover.jpg" \
  --platform youtube
```

Upload as unlisted (for preview):
```bash
python manual_upload.py \
  --video "drive://folder/video.mp4" \
  --title "Episode 4" \
  --description "..." \
  --thumbnail "drive://folder/cover.jpg" \
  --privacy unlisted \
  --platform youtube
```

### Upload to Both Platforms

```bash
python manual_upload.py \
  --video "drive://biggest moments of 2025_reels/reel_1/video.mp4" \
  --title "S1 E4: Biggest Moments of 2025" \
  --description "Full episode description here..." \
  --caption "New episode! Check it out 🎙️ #podcast" \
  --thumbnail "drive://biggest moments of 2025_reels/reel_1/video_cover.jpg" \
  --platform both
```

### Update Instagram Bio

```bash
python manual_upload.py \
  --update-bio \
  --episode 4 \
  --spotify-url "https://open.spotify.com/episode/abc123" \
  --youtube-url "https://youtu.be/def456"
```

## Google Drive Path Format

Use `drive://` prefix for files in Google Drive:

```
drive://folder_name/subfolder/file.mp4
```

**Examples:**
- `drive://biggest moments of 2025_reels/reel_1/video.mp4`
- `drive://my folder/video.mp4`
- `drive://episode 4/cover.jpg`

**Or use local files:**
- `/Users/carrieliu/Downloads/video.mp4`
- `./video.mp4`

## Common Workflows

### Quick Instagram Post

```bash
python manual_upload.py \
  --video "drive://folder/video.mp4" \
  --caption "Check this out! #podcast" \
  --platform instagram
```

### YouTube Preview Then Publish

Step 1: Upload as unlisted
```bash
python manual_upload.py \
  --video "drive://folder/video.mp4" \
  --title "Episode Title" \
  --description "..." \
  --privacy unlisted \
  --platform youtube
```

Step 2: Review the unlisted link

Step 3: Manually change to public in YouTube Studio, or re-upload as public

### Weekly Episode Upload

```bash
# Upload the reel to both platforms
python manual_upload.py \
  --video "drive://episode 5_reels/reel_1/video.mp4" \
  --title "S1 E5: Episode Title" \
  --description "Full description..." \
  --caption "New episode is live! 🎙️" \
  --thumbnail "drive://episode 5_reels/reel_1/video_cover.jpg" \
  --platform both

# Update bio with new links
python manual_upload.py \
  --update-bio \
  --episode 5 \
  --spotify-url "https://..." \
  --youtube-url "https://..."
```

## Tips

1. **Test First**: Try with `--platform youtube --privacy unlisted` to preview before going public

2. **Auto-Thumbnail**: If you don't provide `--thumbnail`, the script will extract a frame from the video

3. **Quotes**: Use quotes around paths with spaces: `"drive://my folder/video.mp4"`

4. **Long Descriptions**: Put multi-line descriptions in a file:
   ```bash
   python manual_upload.py \
     --video "..." \
     --title "..." \
     --description "$(cat description.txt)" \
     --platform youtube
   ```

5. **Check Status**: The script will print success/failure for each platform

## Troubleshooting

**"Error: Folder not found"**
- Check folder names match exactly (case-sensitive)
- Make sure service account has access to Drive folder

**"Error: File not found"**
- Verify the file path is correct
- Check file exists in Google Drive

**"YouTube upload failed"**
- Make sure you've authorized YouTube (first time only)
- Check video format (MP4 recommended)

**"Instagram upload failed"**
- Verify Instagram credentials are correct
- Check video meets requirements (max 60 seconds)
- Try again after a few minutes

## Comparison: Manual vs Automated

| Feature | Manual Upload | Automated System |
|---------|---------------|------------------|
| When | Anytime you want | Tuesday/Thursday 11 AM |
| How | Run command | Automatic |
| Setup | Same credentials | + GitHub Actions + Sheet |
| Flexibility | Total control | Fixed schedule |
| Use Case | Ad-hoc posts | Regular episodes |

**Best Practice**: Use both!
- **Automated**: For your regular Tuesday/Thursday episode reels
- **Manual**: For bonus content, Stories, or when you want immediate posting

## Next Steps

1. Try a test upload to YouTube as unlisted
2. Review and make sure it works
3. Use manual upload whenever you need it!

---

**Quick Command Template** (save this):
```bash
python manual_upload.py \
  --video "drive://FOLDER/video.mp4" \
  --title "TITLE" \
  --description "DESCRIPTION" \
  --caption "CAPTION" \
  --thumbnail "drive://FOLDER/cover.jpg" \
  --platform both
```

