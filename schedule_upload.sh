#!/bin/bash

# Schedule Upload Script
# Usage: ./schedule_upload.sh "folder_link" "title" "description" "HH:MM" "platform"

if [ $# -lt 4 ]; then
    echo "Usage: ./schedule_upload.sh \"FOLDER_LINK\" \"TITLE/CAPTION\" \"DESCRIPTION\" \"HH:MM\" [PLATFORM]"
    echo ""
    echo "Examples:"
    echo "  ./schedule_upload.sh \"https://drive.google.com/...\" \"My Video\" \"Description\" \"14:30\" \"youtube\""
    echo "  ./schedule_upload.sh \"https://drive.google.com/...\" \"Caption #hashtags\" \"Description\" \"14:30\" \"instagram\""
    echo "  ./schedule_upload.sh \"https://drive.google.com/...\" \"Caption #hashtags\" \"Description\" \"14:30\" \"tiktok\""
    echo "  ./schedule_upload.sh \"https://drive.google.com/...\" \"My Video\" \"Description\" \"14:30\" \"all\""
    echo ""
    echo "Platform options: youtube, instagram, tiktok, all (default: youtube)"
    exit 1
fi

FOLDER="$1"
TITLE="$2"
DESCRIPTION="$3"
TIME="$4"
PLATFORM="${5:-youtube}"

# Convert time to cron format
HOUR=$(echo $TIME | cut -d: -f1)
MINUTE=$(echo $TIME | cut -d: -f2)

# Create the command based on platform
if [ "$PLATFORM" = "youtube" ]; then
    CMD="cd /Users/carrieliu/cinrol-video-automation && python3 manual_upload.py --folder \"$FOLDER\" --title \"$TITLE\" --description \"$DESCRIPTION\" --platform youtube >> logs/scheduled_$(date +%Y%m%d_%H%M%S).log 2>&1"
elif [ "$PLATFORM" = "instagram" ]; then
    CMD="cd /Users/carrieliu/cinrol-video-automation && python3 manual_upload.py --folder \"$FOLDER\" --caption \"$TITLE\" --platform instagram >> logs/scheduled_$(date +%Y%m%d_%H%M%S).log 2>&1"
elif [ "$PLATFORM" = "tiktok" ]; then
    CMD="cd /Users/carrieliu/cinrol-video-automation && python3 manual_upload.py --folder \"$FOLDER\" --caption \"$TITLE\" --description \"$DESCRIPTION\" --platform tiktok >> logs/scheduled_$(date +%Y%m%d_%H%M%S).log 2>&1"
elif [ "$PLATFORM" = "all" ]; then
    CMD="cd /Users/carrieliu/cinrol-video-automation && python3 manual_upload.py --folder \"$FOLDER\" --title \"$TITLE\" --caption \"$TITLE\" --description \"$DESCRIPTION\" --platform all >> logs/scheduled_$(date +%Y%m%d_%H%M%S).log 2>&1"
else
    CMD="cd /Users/carrieliu/cinrol-video-automation && python3 manual_upload.py --folder \"$FOLDER\" --title \"$TITLE\" --description \"$DESCRIPTION\" --platform $PLATFORM >> logs/scheduled_$(date +%Y%m%d_%H%M%S).log 2>&1"
fi

# Add to crontab (one-time job for today)
# First, get existing crontab
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null || touch "$TEMP_CRON"

# Add the new job
echo "$MINUTE $HOUR * * * $CMD" >> "$TEMP_CRON"

# Install updated crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✅ Upload scheduled!"
echo ""
echo "📅 Will upload at: $TIME today"
echo "📁 Folder: $FOLDER"
echo "📺 Platform: $PLATFORM"
echo "📝 Title: $TITLE"
echo ""
echo "To view scheduled jobs: crontab -l"
echo "To cancel: crontab -e (then delete the line)"

