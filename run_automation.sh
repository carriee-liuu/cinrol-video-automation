#!/bin/bash

# Cron Job Wrapper Script for Video Automation
# This script runs every Tuesday and Thursday at 11 AM EST

# Set working directory
cd /Users/carrieliu/cinrol-video-automation

# Create log directory if it doesn't exist
mkdir -p logs

# Set log file with timestamp
LOG_FILE="logs/automation_$(date +%Y%m%d_%H%M%S).log"

# Log start time
echo "========================================" >> "$LOG_FILE"
echo "Video Automation Started" >> "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run the automation script
python3 main.py >> "$LOG_FILE" 2>&1

# Capture exit code
EXIT_CODE=$?

# Log completion
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "Video Automation Completed" >> "$LOG_FILE"
echo "Exit Code: $EXIT_CODE" >> "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Keep only last 30 days of logs
find logs -name "automation_*.log" -mtime +30 -delete

exit $EXIT_CODE



