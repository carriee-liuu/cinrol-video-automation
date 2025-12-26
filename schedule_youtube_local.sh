#!/bin/bash
# Local scheduling for YouTube Shorts
# Uploads as PRIVATE, then schedules local cron job to publish

FOLDER="$1"
TITLE="$2"
DESCRIPTION="$3"
SCHEDULE_DATETIME="$4"  # Format: "YYYY-MM-DD HH:MM"

if [ -z "$FOLDER" ] || [ -z "$TITLE" ] || [ -z "$DESCRIPTION" ] || [ -z "$SCHEDULE_DATETIME" ]; then
    echo "Usage: $0 \"FOLDER_LINK\" \"TITLE\" \"DESCRIPTION\" \"YYYY-MM-DD HH:MM\""
    exit 1
fi

echo "=================================="
echo "Scheduling YouTube Short (LOCAL)"
echo "=================================="
echo ""

# Step 1: Upload as PRIVATE
echo "Step 1: Uploading video as PRIVATE..."
cd /Users/carrieliu/cinrol-video-automation
UPLOAD_OUTPUT=$(python3 manual_upload.py \
  --folder "$FOLDER" \
  --title "$TITLE" \
  --description "$DESCRIPTION" \
  --privacy private \
  --platform youtube 2>&1)

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

# Step 2: Schedule local cron job to publish
echo "Step 2: Scheduling local publication..."

SCHEDULE_DATE=$(echo "$SCHEDULE_DATETIME" | cut -d' ' -f1)
SCHEDULE_TIME=$(echo "$SCHEDULE_DATETIME" | cut -d' ' -f2)
SCHEDULE_MINUTE=$(echo "$SCHEDULE_TIME" | cut -d':' -f2)
SCHEDULE_HOUR=$(echo "$SCHEDULE_TIME" | cut -d':' -f1)
SCHEDULE_DAY=$(echo "$SCHEDULE_DATE" | cut -d'-' -f3)
SCHEDULE_MONTH=$(echo "$SCHEDULE_DATE" | cut -d'-' -f2)

# Create the cron command
PUBLISH_COMMAND="cd /Users/carrieliu/cinrol-video-automation && python3 publish_video.py $VIDEO_ID >> logs/publish_${VIDEO_ID}.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$SCHEDULE_MINUTE $SCHEDULE_HOUR $SCHEDULE_DAY $SCHEDULE_MONTH * $PUBLISH_COMMAND") | crontab -

echo ""
echo "✅ YouTube Short scheduled successfully!"
echo ""
echo "📅 Will publish: $SCHEDULE_DATETIME EST"
echo "📺 Video ID: $VIDEO_ID"
echo "🔗 URL: https://www.youtube.com/watch?v=$VIDEO_ID"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Video is currently PRIVATE"
echo "   - Your Mac MUST be ON and AWAKE at $SCHEDULE_DATETIME"
echo ""
echo "To view scheduled jobs: crontab -l"
echo "To cancel: crontab -e (then delete the line with $VIDEO_ID)"
