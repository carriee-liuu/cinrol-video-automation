"""
Thumbnail extractor for generating cover images from videos.
"""

import cv2
import os
from typing import Optional
from PIL import Image


class ThumbnailExtractor:
    """Extracts thumbnail images from video files."""
    
    @staticmethod
    def extract_frame(video_path: str, output_path: str, timestamp: float = 1.0) -> bool:
        """
        Extract a frame from video at specified timestamp.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the thumbnail image
            timestamp: Timestamp in seconds to extract frame (default: 1.0)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Open video file
            video = cv2.VideoCapture(video_path)
            
            if not video.isOpened():
                print(f"Error: Could not open video file: {video_path}")
                return False
            
            # Get video properties
            fps = video.get(cv2.CAP_PROP_FPS)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            print(f"Video info: {duration:.2f}s duration, {fps:.2f} fps")
            
            # Calculate frame number for the timestamp
            frame_number = int(timestamp * fps)
            
            # Make sure we don't exceed video duration
            if frame_number >= total_frames:
                frame_number = min(int(fps), total_frames - 1)  # Use 1 second or last frame
                print(f"Adjusted frame number to {frame_number}")
            
            # Set video position
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # Read the frame
            success, frame = video.read()
            video.release()
            
            if not success:
                print(f"Error: Could not read frame at timestamp {timestamp}s")
                return False
            
            # Save the frame as image
            cv2.imwrite(output_path, frame)
            print(f"Extracted thumbnail to: {output_path}")
            
            # Optimize the image (optional - reduce file size)
            ThumbnailExtractor._optimize_image(output_path)
            
            return True
            
        except Exception as e:
            print(f"Error extracting thumbnail: {e}")
            return False
    
    @staticmethod
    def _optimize_image(image_path: str, max_width: int = 1920, quality: int = 85):
        """
        Optimize image by resizing and compressing.
        
        Args:
            image_path: Path to the image file
            max_width: Maximum width in pixels
            quality: JPEG quality (1-100)
        """
        try:
            img = Image.open(image_path)
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary (for JPEG)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save optimized version
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            print(f"Optimized thumbnail image")
            
        except Exception as e:
            print(f"Warning: Could not optimize image: {e}")
    
    @staticmethod
    def create_thumbnail(video_path: str, cover_path: Optional[str], temp_dir: str) -> Optional[str]:
        """
        Create or use thumbnail for video upload.
        
        If cover_path is provided, use it. Otherwise, extract from video.
        
        Args:
            video_path: Path to the video file
            cover_path: Path to custom cover image (can be None)
            temp_dir: Directory to save extracted thumbnail
        
        Returns:
            Path to the thumbnail image, or None if failed
        """
        if cover_path and os.path.exists(cover_path):
            print(f"Using custom cover image: {cover_path}")
            return cover_path
        
        # Extract thumbnail from video
        print("No custom cover found, extracting thumbnail from video...")
        thumbnail_path = os.path.join(temp_dir, "thumbnail.jpg")
        
        if ThumbnailExtractor.extract_frame(video_path, thumbnail_path, timestamp=1.0):
            return thumbnail_path
        
        return None

