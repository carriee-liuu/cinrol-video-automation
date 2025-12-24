# Google Sheet Template Guide

This document explains how to set up and maintain your Google Sheet for the video automation system.

## Sheet Structure

Your sheet should have the following columns (A through J):

| Column | Header | Type | Required | Example | Notes |
|--------|--------|------|----------|---------|-------|
| A | what (CINROLLING) | Text | Yes | "biggest moments of 2025" | Used as YouTube video title |
| B | type | Text | Yes | "Podcast" | Must be exactly "Podcast" for automation |
| C | planned publish date | Date | Yes | "12/23/2025" | Tuesday date (also used for Thursday) |
| D | Files link | Text | No | "2025 lookback" | Manual reference only, not used by script |
| E | YT/spotify | Text | No | "UPLOADED" | Auto-updated by script |
| F | IG/YT shorts | Text | No | "UPLOADED" | Auto-updated by script |
| G | long-form description | Text | Yes | "Join us as we..." | YouTube description (max 5,000 chars) |
| H | short-form description | Text | Yes | "New episode! 🎙️" | Instagram caption (max 2,200 chars) |
| I | short desc 2 | Text | No | "Alternative caption" | Optional alternative Instagram caption |
| J | **Folder Name** | Text | **Yes** | "biggest moments of 2025" | **NEW - Exact folder name in Google Drive** |

## Important Notes

### Column J: Folder Name
This is the **most critical column** to add. It must contain the exact name of your podcast folder in Google Drive (without the `_reels` suffix).

**Example:**
- Google Drive folder: `biggest moments of 2025`
- Column J value: `biggest moments of 2025`

### Date Format
Dates in Column C should be in **M/D/YYYY** format:
- ✅ Good: `12/23/2025`, `1/6/2026`
- ❌ Bad: `2025-12-23`, `23/12/2025`

### Type Column
Column B must be exactly **"Podcast"** (case-sensitive) for the script to process the row.

### Tuesday/Thursday Logic
- **Only add rows for Tuesday dates**
- The script will use the same row for both Tuesday and Thursday
- Example: Row with date `12/24/2025` (Tuesday) will be used for:
  - Tuesday 12/24: Upload `reel_1`
  - Thursday 12/26: Upload `reel_2`

## Sample Rows

Here are example rows for your sheet:

### Row 1 (Header)
```
what (CINROLLING) | type | planned publish date | Files link | YT/spotify | IG/YT shorts | long-form description | short-form description | short desc 2 | Folder Name
```

### Row 2 (Example Episode)
```
biggest moments of 2025 | Podcast | 12/23/2025 | 2025 lookback | Pending | Pending | Join us as we look back on the defining, formative, joyful stressful big & most memorable moments of our 2025. Listen on Youtube: Find us on Instagram: www.instagram.com/cinder_and_carol/ | we dont know yet podcast join as we look back on the defining, formative, joyful stressful big & most memorable moments of our 2025. #cinrolling #podcast | Alternative caption text | biggest moments of 2025
```

### Row 3 (Another Example)
```
2025 lessons learned + 2026 intentions | Podcast | 12/30/2025 | 2026 resolutions | Pending | Pending | In this episode we reflect on our biggest lessons from 2025 and set intentions for 2026. | New episode: Setting intentions for 2026! 🎯 #cinrolling #newyear | | 2025 lessons learned + 2026 intentions
```

## Character Limits

The script automatically enforces these limits:

- **YouTube Title** (Column A): 100 characters (truncated with "...")
- **YouTube Description** (Column G): 5,000 characters
- **Instagram Caption** (Column H): 2,200 characters

Try to stay within these limits when writing content.

## Hashtags

You can include hashtags directly in your captions (Column H), or the system can append them automatically if you add a hashtags column in the future.

Example caption with hashtags:
```
New episode is live! 🎙️ Check out these tips for success. #cinrolling #podcast #startup #tech
```

## Status Tracking

Columns E and F are automatically updated by the script:
- Before upload: Leave blank or set to "Pending"
- After successful upload: Script updates to "UPLOADED"
- If upload fails: Script may set to "FAILED" (future enhancement)

## Sharing Permissions

**IMPORTANT**: You must share your Google Sheet with the service account email from your Google Cloud credentials.

1. Open your service account JSON file
2. Find the `client_email` field (looks like: `your-service@project.iam.gserviceaccount.com`)
3. Share the Google Sheet with this email address with **Editor** permissions

## Testing

To test your setup:
1. Add a row with today's date (or next Tuesday)
2. Set Column B to "Podcast"
3. Fill in all required columns (A, C, G, H, J)
4. Run the script manually: `python main.py`
5. Check that the status columns update after upload

## Troubleshooting

### "No video found for today's date"
- Check that Column C has the correct date
- Verify Column B says "Podcast" exactly
- Make sure it's a Tuesday date (or Thursday looking back 2 days)

### "Could not find folder"
- Verify Column J matches the exact folder name in Google Drive
- Check that the folder structure exists: `[Folder Name]_reels/reel_1/` and `reel_2/`

### "Missing YouTube title/description"
- Make sure Columns A and G are filled in
- Check for any formula errors in these cells

### Sheet not updating
- Verify the service account has Editor access to the sheet
- Check that the GOOGLE_SHEETS_ID secret is correct

