#!/bin/bash

# Schedule Shorts Upload Script
# Uploads as PRIVATE and schedules to publish at specified time
# Usage: ./schedule_shorts.sh "FOLDER_LINK" "TITLE" "DESCRIPTION" "YYYY-MM-DD HH:MM"

if [ $# -lt 4 ]; then
    echo "Usage: ./schedule_shorts.sh \"FOLDER_LINK\" \"TITLE\" \"DESCRIPTION\" \"YYYY-MM-DD HH:MM\""
    echo ""
    echo "Example:"
    echo "  ./schedule_shorts.sh \"https://drive.google.com/...\" \"My Video Title\" \"Description here\" \"2024-12-25 11:00\""
    echo ""
    echo "Note: Your computer must be ON and AWAKE at the scheduled time!"
    exit 1
fi

FOLDER="$1"
TITLE="$2"
DESCRIPTION="$3"
SCHEDULE_TIME="$4"

echo "=================================="
echo "Scheduling YouTube Short"
echo "=================================="
echo ""
echo "Step 1: Uploading video as PRIVATE..."
echo ""

# Upload video as private (no schedule parameter)
cd /Users/carrieliu/cinrol-video-automation
UPLOAD_OUTPUT=$(python3 manual_upload.py \
  --folder "$FOLDER" \
  --title "$TITLE" \
  --description "$DESCRIPTION" \
  --privacy private \
  --platform youtube 2>&1)

# Extract video ID from output
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
echo "Step 2: Scheduling publication..."
echo ""

# Parse schedule time
SCHEDULE_DATE=$(echo "$SCHEDULE_TIME" | cut -d' ' -f1)
SCHEDULE_HOUR=$(echo "$SCHEDULE_TIME" | cut -d' ' -f2 | cut -d: -f1)
SCHEDULE_MINUTE=$(echo "$SCHEDULE_TIME" | cut -d' ' -f2 | cut -d: -f2)

# Convert date to day, month
MONTH=$(date -j -f "%Y-%m-%d" "$SCHEDULE_DATE" "+%m")
DAY=$(date -j -f "%Y-%m-%d" "$SCHEDULE_DATE" "+%d")

# Create the publish command
PUBLISH_CMD="cd /Users/carrieliu/cinrol-video-automation && python3 publish_video.py $VIDEO_ID >> logs/publish_${VIDEO_ID}.log 2>&1"

# Add to crontab
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null || touch "$TEMP_CRON"

# Add the one-time job
echo "$SCHEDULE_MINUTE $SCHEDULE_HOUR $DAY $MONTH * $PUBLISH_CMD" >> "$TEMP_CRON"

# Install updated crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✅ Short scheduled successfully!"
echo ""
echo "📅 Will publish: $SCHEDULE_TIME EST"
echo "📺 Video ID: $VIDEO_ID"
echo "🔗 URL: https://www.youtube.com/watch?v=$VIDEO_ID"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Video is currently PRIVATE"
echo "   - Your Mac MUST be ON and AWAKE at $SCHEDULE_TIME"
echo "   - Prevent your Mac from sleeping: System Settings > Lock Screen > Turn display off: Never"
echo ""
echo "To view scheduled jobs: crontab -l"
echo "To cancel: crontab -e (then delete the line)"

