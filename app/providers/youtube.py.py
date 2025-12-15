class YouTubeTranscriptFetcher:
    """Fetch transcripts from YouTube."""
    
    def __init__(self):
        pass
    
    def fetch(self, video_id: str) -> str:
        """Fetch transcript from YouTube."""
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([segment['text'] for segment in transcript_list])
            return full_text
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            # Try auto-generated captions
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_generated_transcript(['en'])
                full_text = " ".join([segment['text'] for segment in transcript.fetch()])
                return full_text
            except:
                raise Exception(f"Could not fetch transcript: {str(e)}")
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL."""
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([\w-]{11})',
            r'(?:youtu\.be\/)([\w-]{11})',
            r'(?:youtube\.com\/embed\/)([\w-]{11})',
        ]
        return any(re.search(pattern, url) for pattern in patterns)