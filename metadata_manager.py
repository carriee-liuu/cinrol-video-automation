"""
Google Sheets metadata manager for reading video information.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import gspread
from google.oauth2 import service_account
from config import get_config


class MetadataManager:
    """Manages video metadata from Google Sheets."""
    
    # Column mappings (0-indexed)
    COL_WHAT = 0           # A: what (CINROLLING)
    COL_TYPE = 1           # B: type
    COL_DATE = 2           # C: planned publish date
    COL_FILES_LINK = 3     # D: Files link
    COL_YT_STATUS = 4      # E: YT/spotify
    COL_IG_STATUS = 5      # F: IG/YT shorts
    COL_LONG_DESC = 6      # G: long-form description
    COL_SHORT_DESC = 7     # H: short-form description
    COL_SHORT_DESC_2 = 8   # I: short desc 2
    COL_FOLDER_NAME = 9    # J: Folder Name
    
    def __init__(self):
        self.config = get_config()
        self.client = self._authenticate()
        self.sheet = self._open_sheet()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API using service account."""
        credentials_info = self.config.get_google_credentials()
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(credentials)
    
    def _open_sheet(self):
        """Open the Google Sheet."""
        try:
            return self.client.open_by_key(self.config.sheets_id).sheet1
        except Exception as e:
            raise Exception(f"Failed to open Google Sheet: {e}")
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string from sheet (supports multiple formats).
        
        Args:
            date_str: Date string (e.g., "12/23/2025", "2025-12-23")
        
        Returns:
            datetime object or None if parsing fails
        """
        formats = [
            '%m/%d/%Y',    # 12/23/2025
            '%Y-%m-%d',    # 2025-12-23
            '%m-%d-%Y',    # 12-23-2025
            '%d/%m/%Y',    # 23/12/2025
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        print(f"Warning: Could not parse date '{date_str}'")
        return None
    
    def get_lookup_date(self, current_date: datetime) -> datetime:
        """
        Determine which date to look up in the sheet based on day of week.
        
        Tuesday: Use current date
        Thursday: Use date from 2 days ago (previous Tuesday)
        
        Args:
            current_date: Current datetime
        
        Returns:
            Date to look up in the sheet
        """
        day_of_week = current_date.weekday()  # 0=Monday, 1=Tuesday, 3=Thursday
        
        if day_of_week == 1:  # Tuesday
            return current_date
        elif day_of_week == 3:  # Thursday
            return current_date - timedelta(days=2)
        else:
            # For testing, allow any day
            print(f"Warning: Script is designed for Tuesday/Thursday, today is {current_date.strftime('%A')}")
            return current_date
    
    def get_reel_number(self, current_date: datetime) -> int:
        """
        Determine which reel to use (1 or 2) based on day of week.
        
        Returns:
            1 for Tuesday, 2 for Thursday
        """
        day_of_week = current_date.weekday()
        
        if day_of_week == 1:  # Tuesday
            return 1
        elif day_of_week == 3:  # Thursday
            return 2
        else:
            # Default to 1 for testing
            return 1
    
    def find_video_metadata(self, target_date: Optional[datetime] = None) -> Optional[Dict]:
        """
        Find video metadata for the specified date.
        
        Args:
            target_date: Date to look for. If None, uses today's date with appropriate logic.
        
        Returns:
            Dictionary with video metadata or None if not found
        """
        if target_date is None:
            target_date = datetime.now()
        
        # Determine lookup date and reel number
        lookup_date = self.get_lookup_date(target_date)
        reel_number = self.get_reel_number(target_date)
        
        print(f"Current date: {target_date.strftime('%A, %m/%d/%Y')}")
        print(f"Looking up date: {lookup_date.strftime('%m/%d/%Y')}")
        print(f"Reel number: {reel_number}")
        
        # Get all rows from the sheet
        try:
            all_rows = self.sheet.get_all_values()
        except Exception as e:
            print(f"Error reading sheet: {e}")
            return None
        
        # Skip header row
        for i, row in enumerate(all_rows[1:], start=2):
            # Check if row has enough columns
            if len(row) <= self.COL_FOLDER_NAME:
                continue
            
            # Check if type is "Podcast"
            row_type = row[self.COL_TYPE].strip()
            if row_type.lower() != 'podcast':
                continue
            
            # Parse and compare date
            row_date_str = row[self.COL_DATE].strip()
            row_date = self._parse_date(row_date_str)
            
            if row_date and row_date.date() == lookup_date.date():
                # Found matching row!
                folder_name = row[self.COL_FOLDER_NAME].strip()
                
                if not folder_name:
                    print(f"Warning: Row {i} has matching date but no folder name in Column J")
                    continue
                
                # Extract metadata
                metadata = {
                    'row_number': i,
                    'date': lookup_date,
                    'reel_number': reel_number,
                    'folder_name': folder_name,
                    'youtube_title': row[self.COL_WHAT].strip(),
                    'youtube_description': row[self.COL_LONG_DESC].strip(),
                    'instagram_caption': row[self.COL_SHORT_DESC].strip(),
                    'instagram_caption_alt': row[self.COL_SHORT_DESC_2].strip() if len(row) > self.COL_SHORT_DESC_2 else '',
                    'youtube_status': row[self.COL_YT_STATUS].strip(),
                    'instagram_status': row[self.COL_IG_STATUS].strip(),
                }
                
                # Validate required fields
                if not metadata['youtube_title']:
                    print(f"Warning: Row {i} missing YouTube title (Column A)")
                if not metadata['youtube_description']:
                    print(f"Warning: Row {i} missing YouTube description (Column G)")
                if not metadata['instagram_caption']:
                    print(f"Warning: Row {i} missing Instagram caption (Column H)")
                
                # Apply character limits
                metadata['youtube_title'] = self.config.validate_youtube_title(metadata['youtube_title'])
                metadata['youtube_description'] = self.config.validate_youtube_description(metadata['youtube_description'])
                metadata['instagram_caption'] = self.config.validate_instagram_caption(metadata['instagram_caption'])
                
                print(f"Found metadata in row {i}:")
                print(f"  Folder: {metadata['folder_name']}")
                print(f"  YouTube Title: {metadata['youtube_title']}")
                print(f"  Reel: {reel_number}")
                
                return metadata
        
        print(f"No matching row found for date {lookup_date.strftime('%m/%d/%Y')} with type='Podcast'")
        return None
    
    def update_status(self, row_number: int, platform: str, status: str = "UPLOADED") -> bool:
        """
        Update the upload status in the sheet.
        
        Args:
            row_number: Row number to update (1-indexed)
            platform: 'youtube' or 'instagram'
            status: Status text (default: "UPLOADED")
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if platform.lower() == 'youtube':
                col = self.COL_YT_STATUS + 1  # Convert to 1-indexed
            elif platform.lower() == 'instagram':
                col = self.COL_IG_STATUS + 1
            else:
                print(f"Unknown platform: {platform}")
                return False
            
            self.sheet.update_cell(row_number, col, status)
            print(f"Updated {platform} status to '{status}' in row {row_number}")
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            return False

