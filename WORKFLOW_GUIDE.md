# Content Creation & Posting Workflow

This guide documents the complete workflow for creating and posting videos using AI assistance (Cursor or Claude Code) and the automation system.

## 🎯 Overview

Your workflow involves:
1. **Preparing content** - Video in Google Drive, metadata in Google Sheet
2. **AI-assisted caption creation** - Using Cursor/Claude Code to generate captions and hashtags
3. **Updating Google Sheet** - Adding video metadata for scheduled or manual posts
4. **Posting** - Either scheduled (automatic) or manual (immediate)

## 📋 Step-by-Step Workflow

### Step 1: Prepare Your Video

1. **Upload video to Google Drive**
   - Create a folder for your episode (e.g., `maintaining friendships in your 20s`)
   - Upload your video file (MP4 format)
   - Optionally add a cover image (name it with `cover` or `thumbnail` in the filename)

2. **Create the folder structure** (if using scheduled uploads):
   ```
   [Root Folder]/
     └── maintaining friendships in your 20s/
         └── maintaining friendships in your 20s_reels/
             ├── reel_1/  (for Tuesday)
             │   └── video.mp4
             └── reel_2/  (for Thursday)
                 └── video.mp4
   ```

### Step 2: Get AI Help with Captions & Hashtags

**Using Cursor or Claude Code:**

1. **Open a new chat** in Cursor/Claude Code
2. **Provide context** about your video:
   ```
   I have a video about [topic]. Can you help me create:
   - An Instagram caption (with hashtags)
   - A YouTube title
   - A YouTube description
   
   Context: [describe your video content]
   ```

3. **Example prompt:**
   ```
   I have a podcast episode about maintaining friendships in your 20s. 
   We talk about how life stages change friendships and lessons learned.
   
   Can you:
   1. Create an engaging Instagram caption with trending hashtags
   2. Suggest a YouTube title
   3. Write a YouTube description
   
   Make it authentic and relatable for people in their 20s.
   ```

4. **Refine the output:**
   - Ask for revisions: "Make it more casual" or "Add more hashtags"
   - Request specific formats: "Give me a version under 100 characters"
   - Get variations: "Give me 3 caption options"

5. **Get hashtag suggestions:**
   ```
   Can you add trending and related hashtags for [topic]?
   Focus on: [your niche/keywords]
   ```

### Step 3: Update Google Sheet

**For Scheduled Uploads (Tuesday/Thursday 11 AM):**

1. **Open your Google Sheet**
2. **Add a new row** with:
   - **Column A** (what/CINROLLING): Video title (e.g., "maintaining friendships in your 20s")
   - **Column B** (type): `Podcast`
   - **Column C** (planned publish date): Tuesday date in M/D/YYYY format (e.g., `1/28/2026`)
   - **Column G** (long-form description): YouTube description (from AI)
   - **Column H** (short-form description): Instagram caption (from AI)
   - **Column J** (Folder Name): Exact folder name from Google Drive (e.g., `maintaining friendships in your 20s`)

3. **Example row:**
   | A | B | C | G | H | J |
   |---|---|---|------|------|------|
   | maintaining friendships in your 20s | Podcast | 1/28/2026 | Full YouTube description... | Instagram caption with #hashtags | maintaining friendships in your 20s |

**Important Notes:**
- Only add rows for **Tuesday dates** (the script uses the same row for Thursday)
- Column J must match your Google Drive folder name exactly
- Dates must be in M/D/YYYY format

### Step 4: Post Your Video

#### Option A: Scheduled Upload (Automatic)

**For Tuesday/Thursday 11 AM posts:**

1. **Ensure your Google Sheet is updated** (Step 3)
2. **Verify folder structure** matches expected format
3. **Make sure your Mac is ON and awake** at 11 AM EST
4. **The script runs automatically** - no action needed!

**What happens:**
- Script reads Google Sheet at 11 AM EST
- Downloads video from Google Drive
- Uploads to YouTube and Instagram
- Updates status columns (E & F) to "UPLOADED"

#### Option B: Manual Upload (Immediate)

**For posting right now:**

1. **Get your Google Drive folder link:**
   - Right-click folder → Get link
   - Copy the full URL

2. **Use the manual upload script:**
   ```bash
   python3 manual_upload.py \
     --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
     --title "Video Title" \
     --description "Full YouTube description..." \
     --caption "Instagram caption with #hashtags" \
     --platform all
   ```

3. **Or use AI to generate the command:**
   ```
   In Cursor/Claude Code, ask:
   "Help me create the command to upload this video:
   - Folder link: [paste link]
   - Title: [your title]
   - Description: [your description]
   - Caption: [your caption]"
   ```

### Step 5: Verify & Update Sheet

After posting:

1. **Check upload status:**
   - YouTube: Video appears on your channel
   - Instagram: Reel appears on your profile

2. **Update Google Sheet** (if needed):
   - Add YouTube URL to Column M (if tracking)
   - Add Instagram URL to Column K (if tracking)
   - Status columns (E & F) update automatically for scheduled posts

## 🤖 Using AI Assistants Effectively

### Best Practices

1. **Provide context:**
   - Video topic and key points
   - Target audience
   - Tone/style preferences
   - Any specific requirements

2. **Iterate:**
   - Don't accept the first draft
   - Ask for revisions: "Make it shorter", "More casual", "Add emojis"
   - Request multiple options

3. **Use specific prompts:**
   ```
   ❌ Bad: "Write a caption"
   ✅ Good: "Write an Instagram caption for a podcast episode about 
            maintaining friendships in your 20s. Include 10-15 relevant 
            hashtags. Keep it under 200 characters. Make it relatable 
            and authentic."
   ```

4. **Get variations:**
   - Ask for 3-5 caption options
   - Request different hashtag sets
   - Get condensed versions (100 chars, 50 chars)

### Example AI Prompts

**Caption Creation:**
```
Create an Instagram caption for a podcast episode about [topic].
- Include 10-15 trending hashtags
- Keep it under 2200 characters
- Make it engaging and authentic
- Add a call-to-action
- Include emojis sparingly
```

**Hashtag Research:**
```
Give me trending and related hashtags for [topic].
Focus on:
- [niche keywords]
- [target audience]
- [content type]
Include mix of popular and niche hashtags.
```

**Condensed Versions:**
```
Give me a condensed version of this caption:
[your caption]

Requirements:
- Under 100 characters
- Keep the main message
- Include 3-5 key hashtags
```

**Creator Bio:**
```
Create a creator bio for brand collaborations:
- [your niche/topic]
- [your unique value]
- [your audience]
Keep it under 240 characters
```

## 📝 Google Sheet Template

Your Google Sheet should have these columns:

| Column | Header | What to Fill | Example |
|--------|--------|-------------|---------|
| A | what (CINROLLING) | Video title | maintaining friendships in your 20s |
| B | type | Always "Podcast" | Podcast |
| C | planned publish date | Tuesday date (M/D/YYYY) | 1/28/2026 |
| D | Files link | (Optional) Reference | - |
| E | YT/spotify | Auto-updated | UPLOADED |
| F | IG/YT shorts | Auto-updated | UPLOADED |
| G | long-form description | YouTube description | Full description... |
| H | short-form description | Instagram caption | Caption with #hashtags |
| I | short desc 2 | (Optional) Alternative | - |
| J | Folder Name | Exact Drive folder name | maintaining friendships in your 20s |

## 🎨 Caption Best Practices

### Instagram Captions

**Structure:**
1. **Hook** - First line grabs attention
2. **Content** - Main message (2-3 sentences)
3. **Call-to-action** - "Link in bio", "Watch full episode"
4. **Hashtags** - 10-15 relevant hashtags

**Example:**
```
we've talked about making friends, now how do we maintain them? 🤔 
join us as we talk about the hard reality of what changing life 
stages and building our own lives does to maintaining friendships 
in our 20s. and some of our #lessonslearned

NEW kinda vulnerable EPISODE AVAILABLE wherever you listen ✨ 
link in bio

#Friendship #FriendshipGoals #FriendshipAdvice #MaintainingFriendships 
#FriendshipTips #AdultFriendships #FriendshipStruggles 
#FriendshipJourney #InYour20s #20sLife #Adulting #LifeStages 
#LessonsLearned #Vulnerability #Podcast #NewEpisode
```

### YouTube Descriptions

**Structure:**
1. **Main description** - 2-3 paragraphs about the video
2. **Call-to-action** - Links, subscribe, etc.
3. **Timestamps** (if applicable)
4. **Links** - Spotify, Instagram, etc.

**Example:**
```
we've talked about making friends, now how do we maintain them? 
join us as we talk about the hard reality of what changing life 
stages and building our own lives does to maintaining friendships 
in our 20s. and some of our lessons learned

NEW EPISODE AVAILABLE wherever you listen ✨ link in bio

[Links section]
```

## 🔄 Complete Workflow Example

**Scenario:** Posting a video about "maintaining friendships in your 20s"

1. **Video ready** in Google Drive folder: `maintaining friendships in your 20s`

2. **Ask AI for captions:**
   ```
   Help me create captions for a podcast episode about maintaining 
   friendships in your 20s. We discuss how life stages change 
   friendships and lessons learned.
   ```

3. **Get AI output:**
   - Instagram caption with hashtags
   - YouTube title
   - YouTube description

4. **Update Google Sheet:**
   - Add row with Tuesday date (1/28/2026)
   - Fill in columns A, B, C, G, H, J

5. **Post:**
   - **Scheduled:** Wait for Tuesday 11 AM (automatic)
   - **Manual:** Run `manual_upload.py` with folder link and captions

6. **Verify:**
   - Check YouTube channel
   - Check Instagram profile
   - Confirm status updated in sheet

## 💡 Pro Tips

1. **Batch create captions:** Ask AI to create captions for multiple videos at once
2. **Save templates:** Keep caption templates for different content types
3. **Track performance:** Use Google Sheet to track which captions perform best
4. **Schedule in advance:** Update Google Sheet days/weeks ahead for scheduled posts
5. **Use AI for variations:** Get multiple caption options and A/B test them

## 🆘 Troubleshooting

**Caption too long:**
- Ask AI: "Give me a condensed version under [X] characters"

**Need more hashtags:**
- Ask AI: "Add 10 more trending hashtags for [topic]"

**Sheet not updating:**
- Verify service account has edit access
- Check date format (M/D/YYYY)
- Ensure Column B says "Podcast" exactly

**Upload failed:**
- Check logs: `logs/automation_*.log`
- Verify video file exists in Drive
- Confirm folder name matches Column J exactly

---

**Remember:** The AI assistant is your creative partner. Use it to iterate, refine, and perfect your captions before posting!
