import re

def detect_media_source(media_input: str) -> tuple[str, str]:
    """Detect what type of media source this is and extract ID."""
    
    # YouTube patterns
    youtube_patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]{11})',
        r'(?:youtu\.be\/)([\w-]{11})',
        r'(?:youtube\.com\/embed\/)([\w-]{11})',
    ]
    
    # Vimeo patterns (for future expansion)
    vimeo_patterns = [
        r'(?:vimeo\.com\/)(\d+)',
        r'(?:player\.vimeo\.com\/video\/)(\d+)',
    ]
    
    # Check YouTube
    for pattern in youtube_patterns:
        match = re.search(pattern, media_input)
        if match:
            return 'youtube', match.group(1)
    
    # Check Vimeo (future)
    for pattern in vimeo_patterns:
        match = re.search(pattern, media_input)
        if match:
            return 'vimeo', match.group(1)
    
    # Check if it's just an ID (assume YouTube for now)
    if re.match(r'^[\w-]{11}$', media_input):
        return 'youtube', media_input
    
    # Check if it's a local file path
    if media_input.endswith(('.mp3', '.wav', '.mp4', '.m4a')):
        return 'audio_file', media_input
    
    raise ValueError(f"Could not detect media source from: {media_input}")