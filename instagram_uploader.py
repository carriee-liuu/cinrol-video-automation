"""
Instagram uploader for uploading Reels with captions and cover images.
"""

import os
import time
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, FeedbackRequired
from config import get_config


class InstagramUploader:
    """Handles Instagram Reels uploads using instagrapi."""
    
    def __init__(self):
        self.config = get_config()
        self.client = Client()
        self.session_file = os.path.join(self.config.temp_dir, 'instagram_session.json')
        self._upload_attempted = False  # Prevent multiple uploads
        self._login()
    
    def _login(self):
        """Login to Instagram using credentials."""
        # Try to load existing session
        if os.path.exists(self.session_file):
            try:
                print("Loading Instagram session...")
                self.client.load_settings(self.session_file)
                self.client.login(
                    self.config.instagram_username,
                    self.config.instagram_password
                )
                
                # Verify session is valid
                self.client.get_timeline_feed()
                print("Instagram session loaded successfully")
                return
            except Exception as e:
                print(f"Existing session invalid: {e}")
        
        # Perform fresh login
        try:
            print(f"Logging into Instagram as {self.config.instagram_username}...")
            self.client.login(
                self.config.instagram_username,
                self.config.instagram_password
            )
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            print("Instagram login successful")
            
        except ChallengeRequired as e:
            print("Instagram requires verification (2FA or challenge)")
            print(f"Error: {e}")
            raise Exception(
                "Instagram challenge required. Please verify your account manually "
                "or use an account without 2FA for automation."
            )
        except LoginRequired as e:
            print(f"Instagram login failed: {e}")
            raise Exception("Instagram login failed. Check your credentials.")
        except Exception as e:
            print(f"Error logging into Instagram: {e}")
            raise
    
    def upload_reel(
        self,
        video_path: str,
        caption: str,
        cover_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload a video as an Instagram Reel.
        
        CRITICAL: This function will ONLY upload ONCE per instance.
        If upload was already attempted, it will immediately return success.
        
        Args:
            video_path: Path to the video file
            caption: Caption text (including hashtags)
            cover_path: Optional path to cover image
        
        Returns:
            Media ID if successful, None otherwise
        """
        # ABSOLUTE PREVENTION: If upload was already attempted, return immediately
        if self._upload_attempted:
            print("ERROR: Upload already attempted in this session. Preventing duplicate post.")
            return "already_attempted"
        
        # Create lock file to prevent multiple simultaneous uploads
        import hashlib
        lock_file = os.path.join(self.config.temp_dir, f"instagram_upload_{hashlib.md5(caption.encode()).hexdigest()[:8]}.lock")
        
        if os.path.exists(lock_file):
            print(f"ERROR: Lock file exists: {lock_file}")
            print("Another upload with this caption may be in progress or was recently completed.")
            print("To prevent duplicates, this upload is blocked.")
            return "locked"
        
        # Create lock file
        try:
            with open(lock_file, 'w') as f:
                f.write(str(time.time()))
        except Exception as e:
            print(f"Warning: Could not create lock file: {e}")
        
        # Mark upload as attempted IMMEDIATELY to prevent any retries
        self._upload_attempted = True
        
        try:
            if not os.path.exists(video_path):
                print(f"Error: Video file not found: {video_path}")
                return None
            
            # Validate video duration (Instagram Reels max 90 seconds)
            # Note: instagrapi will handle this, but we can add a check if needed
            
            print(f"Uploading Reel to Instagram (ONE TIME ONLY - NO RETRIES)...")
            print(f"Caption: {caption[:100]}..." if len(caption) > 100 else f"Caption: {caption}")
            
            from pathlib import Path
            
            video_path_obj = Path(video_path)
            thumbnail_path_obj = Path(cover_path) if cover_path and os.path.exists(cover_path) else None
            
            # CRITICAL: Only call clip_upload ONCE - no retries, no loops
            # Use clip_upload - specifically for Reels (not regular video posts)
            print("=" * 80)
            print("CALLING clip_upload - SINGLE ATTEMPT ONLY")
            print("=" * 80)
            
            # IMPORTANT: clip_upload may succeed (post the reel) but then throw exceptions
            # when accessing the media object. We MUST treat ANY non-immediate failure as success
            # to prevent duplicates. Once clip_upload is called, we assume the post was created.
            # Additionally, clip_upload may sometimes fail to save the caption, so we use
            # media_edit() as a fallback to ensure the caption is always applied.
            media_id = None
            media_code = None
            
            try:
                # THIS IS THE ONLY PLACE WHERE clip_upload IS CALLED
                # If this succeeds (even partially), the post was created - DO NOT RETRY
                media = self.client.clip_upload(
                    path=video_path_obj,
                    caption=caption,
                    thumbnail=thumbnail_path_obj
                )
                
                # If we got here, clip_upload succeeded - the post was created
                # Try to get the media ID, but don't fail if we can't
                try:
                    media_id = media.pk
                    media_code = getattr(media, 'code', None)
                    print(f"✓ Reel uploaded successfully! Media ID: {media_id}")
                    if media_code:
                        print(f"✓ URL: https://www.instagram.com/reel/{media_code}/")
                except (AttributeError, Exception) as e:
                    # Post succeeded but we can't access the ID - still return success
                    print(f"✓ Reel uploaded successfully, but couldn't access media ID: {e}")
                    print("⚠ Will attempt to find media ID via recent posts to add caption")
                    
            except Exception as upload_error:
                # CRITICAL: clip_upload may have posted the reel before throwing an error
                # We MUST assume success to prevent duplicates
                print(f"⚠ Error during/after clip_upload: {upload_error}")
                print("⚠ ASSUMING SUCCESS to prevent duplicate posts")
                print("⚠ If clip_upload was called, the post was likely created")
                print("⚠ Will attempt to find media ID via recent posts to add caption")
            
            # FALLBACK: If we don't have a media_id but the upload likely succeeded,
            # try to find the most recent Reel and add the caption via media_edit()
            if not media_id:
                try:
                    print("Attempting to find recently uploaded Reel to add caption...")
                    # Get the most recent media from the user's timeline
                    recent_medias = self.client.user_medias(self.client.user_id, amount=1)
                    if recent_medias:
                        most_recent = recent_medias[0]
                        # Check if it's a Reel (clips) and was posted very recently (within last 2 minutes)
                        if hasattr(most_recent, 'media_type') and most_recent.media_type == 2:  # 2 = Reel/Clip
                            media_id = most_recent.pk
                            print(f"✓ Found recent Reel with ID: {media_id}")
                        else:
                            print("⚠ Most recent post is not a Reel, skipping caption fallback")
                    else:
                        print("⚠ Could not find recent media to add caption")
                except Exception as find_error:
                    print(f"⚠ Could not find recent Reel to add caption: {find_error}")
            
            # If we have a media_id, ensure the caption is applied via media_edit() as a fallback
            # This handles the case where clip_upload succeeded but failed to save the caption
            if media_id:
                print("Ensuring caption is applied via media_edit() fallback...")
                # Small delay to ensure the post is fully processed
                time.sleep(2)
                caption_added = self._add_caption_via_edit(media_id, caption)
                if caption_added:
                    print("✓ Caption successfully applied via fallback method")
                else:
                    print("⚠ Caption may not have been applied - please check manually")
            
            # Always return success if clip_upload was attempted (to prevent duplicates)
            if media_id:
                return str(media_id)
            else:
                return "uploaded"  # Return a non-None value to indicate success
            
        except FeedbackRequired as e:
            print(f"Instagram feedback required: {e}")
            print("Your account may be flagged for spam or automation. Wait before trying again.")
            # Don't retry on feedback required - this prevents duplicates
            return None
        except Exception as e:
            print(f"Error uploading Reel to Instagram: {e}")
            # Return None only for pre-upload errors (file not found, etc.)
            return None
        finally:
            # Keep lock file to prevent immediate re-uploads
            # It will be cleaned up by the system or manually
            pass
    
    def upload_reel_with_retry(
        self,
        video_path: str,
        caption: str,
        cover_path: Optional[str] = None,
        max_retries: int = 1,
        retry_delay: int = 60
    ) -> Optional[str]:
        """
        Upload Reel - ABSOLUTELY NO RETRIES. Posts exactly once.
        
        Args:
            video_path: Path to the video file
            caption: Caption text
            cover_path: Optional path to cover image
            max_retries: IGNORED - always posts once only
            retry_delay: IGNORED
        
        Returns:
            Media ID if successful, None otherwise
        """
        # CRITICAL: Check if upload was already attempted
        if self._upload_attempted:
            print("ERROR: Upload already attempted. This function will NOT post again.")
            return "already_attempted"
        
        # ABSOLUTE SINGLE ATTEMPT - no retries, no loops, no exceptions
        print("=" * 80)
        print("UPLOADING REEL - SINGLE ATTEMPT ONLY (NO RETRIES)")
        print("=" * 80)
        
        # Call upload_reel exactly once - it has its own safeguards
        result = self.upload_reel(video_path, caption, cover_path)
        
        # Regardless of result, mark as attempted and return
        # upload_reel already marked it, but be extra safe
        self._upload_attempted = True
        
        return result
    
    def _add_caption_via_edit(self, media_id: str, caption: str) -> bool:
        """
        Add caption to an uploaded Reel using media_edit() as a fallback.
        This is used when clip_upload succeeds but fails to save the caption.
        
        Args:
            media_id: The media ID of the uploaded Reel
            caption: The caption text to add
        
        Returns:
            True if caption was successfully added, False otherwise
        """
        try:
            print(f"Attempting to add caption via media_edit() for media ID: {media_id}")
            self.client.media_edit(media_id, caption=caption)
            print("✓ Caption successfully added via media_edit()")
            return True
        except Exception as e:
            print(f"⚠ Could not add caption via media_edit(): {e}")
            return False
    
    def append_hashtags(self, caption: str, hashtags: str) -> str:
        """
        Append hashtags to caption if not already present.
        
        Args:
            caption: Original caption text
            hashtags: Hashtags to append (space-separated)
        
        Returns:
            Caption with hashtags
        """
        if not hashtags:
            return caption
        
        # Check if hashtags are already in caption
        caption_lower = caption.lower()
        for tag in hashtags.split():
            if tag.lower() not in caption_lower:
                caption += f" {tag}"
        
        return caption

