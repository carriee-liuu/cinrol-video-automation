#!/usr/bin/env python3
"""
Update Google Sheet after a video is posted.
Marks status as "Posted" and optionally adds Instagram link.
"""

import sys
import gspread
from config import get_config
from datetime import datetime


def update_sheet_status(youtube_url: str, instagram_url: str = None):
    """
    Update the Posting Schedule sheet after a video is posted.
    
    Args:
        youtube_url: YouTube video URL to find in the sheet
        instagram_url: Optional Instagram post URL to add
    """
    config = get_config()
    gc = gspread.service_account_from_dict(config.get_google_credentials())
    
    sheet_id = "11Oo5xYZo6rIqMSvsuFtULn9k-IjTOgm3LjymiFVa0Fo"
    spreadsheet = gc.open_by_key(sheet_id)
    
    # Find the Posting Schedule sheet
    schedule_sheet = None
    for ws in spreadsheet.worksheets():
        if "posting" in ws.title.lower() and "schedule" in ws.title.lower():
            schedule_sheet = ws
            break
    
    if not schedule_sheet:
        print("Error: Could not find Posting Schedule sheet")
        return False
    
    # Get all values
    all_values = schedule_sheet.get_all_values()
    
    # Find the row with this YouTube URL
    row_num = None
    for i, row in enumerate(all_values[1:], start=2):  # Skip header, start at row 2
        if len(row) > 9 and youtube_url in row[9]:  # Column J (index 9)
            row_num = i
            break
    
    if not row_num:
        print(f"Error: Could not find row with YouTube URL: {youtube_url}")
        return False
    
    # Update the row
    updates = []
    
    # Column K (Instagram Link) - index 10
    if instagram_url:
        schedule_sheet.update(values=[[instagram_url]], range_name=f'K{row_num}')
        print(f"✓ Added Instagram link to row {row_num}")
    
    # Column L (Status) - index 11
    schedule_sheet.update(values=[["Posted"]], range_name=f'L{row_num}')
    print(f"✓ Updated status to 'Posted' for row {row_num}")
    
    # Column M (Notes) - add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p EST")
    schedule_sheet.update(values=[[f"Posted on {timestamp}"]], range_name=f'M{row_num}')
    print(f"✓ Added timestamp: {timestamp}")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 update_sheet_after_post.py YOUTUBE_URL [INSTAGRAM_URL]")
        print("\nExample:")
        print("  python3 update_sheet_after_post.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("  python3 update_sheet_after_post.py https://www.youtube.com/watch?v=VIDEO_ID https://instagram.com/p/POST_ID")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    instagram_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = update_sheet_status(youtube_url, instagram_url)
    sys.exit(0 if success else 1)

