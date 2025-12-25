#!/bin/bash

# Schedule Shorts with GitHub Actions
# Uploads as PRIVATE and triggers GitHub Actions to publish at scheduled time
# Usage: ./schedule_shorts_github.sh "FOLDER_LINK" "TITLE" "DESCRIPTION" "YYYY-MM-DD HH:MM"

if [ $# -lt 4 ]; then
    echo "Usage: ./schedule_shorts_github.sh \"FOLDER_LINK\" \"TITLE\" \"DESCRIPTION\" \"YYYY-MM-DD HH:MM\""
    echo ""
    echo "Example:"
    echo "  ./schedule_shorts_github.sh \"https://drive.google.com/...\" \"My Video\" \"Description\" \"2024-12-25 11:00\""
    echo ""
    echo "Note: Your computer does NOT need to be on! GitHub Actions handles it."
    exit 1
fi

FOLDER="$1"
TITLE="$2"
DESCRIPTION="$3"
SCHEDULE_TIME="$4"

echo "=================================="
echo "Scheduling YouTube Short via GitHub Actions"
echo "=================================="
echo ""
echo "Step 1: Uploading video as PRIVATE..."
echo ""

# Upload video as private
cd /Users/carrieliu/cinrol-video-automation
UPLOAD_OUTPUT=$(python3 manual_upload.py \
  --folder "$FOLDER" \
  --title "$TITLE" \
  --description "$DESCRIPTION" \
  --privacy private \
  --platform youtube 2>&1)

# Extract video ID
VIDEO_ID=$(echo "$UPLOAD_OUTPUT" | grep "Video ID:" | head -1 | awk '{print $NF}')

if [ -z "$VIDEO_ID" ]; then
    echo "✗ Failed to upload video"
    echo "$UPLOAD_OUTPUT"
    exit 1
fi

echo ""
echo "✓ Video uploaded as PRIVATE"
echo "  Video ID: $VIDEO_ID"
echo "  URL: https://www.youtube.com/watch?v=$VIDEO_ID"
echo ""
echo "Step 2: Triggering GitHub Actions workflow..."
echo ""

# Trigger GitHub Actions workflow
gh workflow run publish_video.yml \
  -f video_id="$VIDEO_ID" \
  -f publish_time="$SCHEDULE_TIME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Scheduled successfully via GitHub Actions!"
    echo ""
    echo "📅 Will publish: $SCHEDULE_TIME EST"
    echo "📺 Video ID: $VIDEO_ID"
    echo "🔗 URL: https://www.youtube.com/watch?v=$VIDEO_ID"
    echo ""
    echo "✨ Your Mac does NOT need to be on!"
    echo "   GitHub Actions will publish it automatically."
    echo ""
    echo "To view workflow: gh run list --workflow=publish_video.yml"
else
    echo ""
    echo "✗ Failed to trigger GitHub Actions"
    echo ""
    echo "Make sure:"
    echo "  1. You have 'gh' CLI installed: brew install gh"
    echo "  2. You're logged in: gh auth login"
    echo "  3. The repo is pushed to GitHub"
    echo ""
    echo "Alternative: Manually trigger at https://github.com/carriee-liuu/cinrol-video-automation/actions"
fi

