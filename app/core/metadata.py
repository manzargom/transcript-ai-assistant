import re
import json
from typing import Dict, Any, Optional
import yt_dlp


class VideoMetadataExtractor:
    """Extract metadata from YouTube videos."""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
        }
    
    def extract(self, video_id: str) -> Dict[str, Any]:
        """Extract comprehensive metadata."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={video_id}",
                    download=False
                )
                
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'description': info.get('description', '')[:500],  # Limit length
                    'duration': info.get('duration'),
                    'channel': info.get('channel', 'Unknown Channel'),
                    'channel_id': info.get('channel_id'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'categories': info.get('categories', []),
                    'tags': info.get('tags', [])[:10],  # First 10 tags
                    'thumbnail': info.get('thumbnail'),
                    'webpage_url': info.get('webpage_url'),
                    'is_live': info.get('is_live', False),
                    'age_limit': info.get('age_limit', 0)
                }
                
        except Exception as e:
            # Return minimal metadata if extraction fails
            return {
                'title': f"Video {video_id}",
                'description': None,
                'duration': None,
                'channel': 'Unknown Channel',
                'error': str(e)
            }
    
    def extract_basic(self, video_id: str) -> Dict[str, Any]:
        """Extract only essential metadata (faster)."""
        import urllib.request
        import html
        
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = urllib.request.urlopen(url)
            html_content = response.read().decode('utf-8')
            
            # Extract title
            title_match = re.search(r'<meta name="title" content="([^"]+)"', html_content)
            title = html.unescape(title_match.group(1)) if title_match else f"Video {video_id}"
            
            # Extract channel
            channel_match = re.search(r'"author":"([^"]+)"', html_content)
            channel = channel_match.group(1) if channel_match else "Unknown Channel"
            
            return {
                'title': title,
                'channel': channel,
                'webpage_url': url
            }
            
        except Exception:
            return {
                'title': f"Video {video_id}",
                'channel': 'Unknown Channel',
                'webpage_url': f"https://www.youtube.com/watch?v={video_id}"
            }