#!/bin/bash
# This script should run on Friday morning (between 5:30 AM - 10:59 AM EST)
# to schedule the 11 AM publish

VIDEO_ID="oTwZlvK-B28"
PUBLISH_TIME="2024-12-27 11:00"

echo "Triggering GitHub Actions to publish at $PUBLISH_TIME EST..."
gh workflow run publish_video.yml \
  -f video_id="$VIDEO_ID" \
  -f publish_time="$PUBLISH_TIME"

if [ $? -eq 0 ]; then
    echo "✅ Scheduled! Video will be published at 11:00 AM EST on Friday"
    echo "🔗 https://www.youtube.com/watch?v=$VIDEO_ID"
else
    echo "❌ Failed to schedule"
fi
