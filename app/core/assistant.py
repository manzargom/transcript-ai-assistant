from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from .ollama_client import OllamaClient
from ..providers.youtube import YouTubeTranscriptFetcher
from ..providers.vimeo import VimeoTranscriptFetcher  # Future
from .metadata import MediaMetadataExtractor


@dataclass
class ProcessingResult:
    """Data class for processing results."""
    media_id: str
    media_title: str
    media_description: Optional[str]
    media_duration: Optional[int]
    source: str  # 'youtube', 'vimeo', 'audio_file', etc.
    transcript: str
    summary: str
    script: str
    translation: Optional[str] = None
    target_language: Optional[str] = None
    processing_time: Optional[float] = None
    style_used: Optional[str] = None
    model_used: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class TranscriptAIAssistant:
    """Generic assistant for any transcript source."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", 
                 default_model: str = "mistral:7b-instruct-q4_K_M"):
        self.ollama_client = OllamaClient(ollama_url, default_model)
        self.metadata_extractor = MediaMetadataExtractor()
        self.fetchers = {
            'youtube': YouTubeTranscriptFetcher(),
            # 'vimeo': VimeoTranscriptFetcher(),  # Future
        }
    
    def detect_source(self, media_input: str) -> tuple[str, str]:
        """Detect source type and extract ID."""
        from ..utils.url_utils import detect_media_source
        
        source, media_id = detect_media_source(media_input)
        if source not in self.fetchers:
            raise ValueError(f"Unsupported media source: {source}")
        
        return source, media_id
    
    def fetch_transcript(self, source: str, media_id: str) -> str:
        """Fetch transcript from appropriate source."""
        fetcher = self.fetchers.get(source)
        if not fetcher:
            raise ValueError(f"No fetcher available for source: {source}")
        
        return fetcher.fetch(media_id)
    
    def extract_metadata(self, source: str, media_id: str) -> Dict[str, Any]:
        """Extract metadata from media."""
        return self.metadata_extractor.extract(source, media_id)
    
    def process_media(self, media_input: str, style: str = "educational", 
                     translate: bool = False, target_language: str = "es") -> ProcessingResult:
        """Complete media processing pipeline."""
        import time
        start_time = time.time()
        
        # Detect source and extract ID
        source, media_id = self.detect_source(media_input)
        
        # Get metadata
        print(f"📊 Extracting metadata from {source}...")
        metadata = self.extract_metadata(source, media_id)
        
        # Get transcript
        print(f"📝 Fetching transcript from {source}...")
        transcript = self.fetch_transcript(source, media_id)
        
        # Generate summary
        print("🤖 Generating summary...")
        summary = self._generate_summary(transcript, metadata, source)
        
        # Generate script
        print(f"🎭 Generating {style} script...")
        script = self._generate_script(summary, style, metadata)
        
        # Optional translation
        translation = None
        if translate:
            print(f"🌐 Translating to {target_language}...")
            translation = self._translate_content(script, target_language)
        
        processing_time = time.time() - start_time
        
        return ProcessingResult(
            media_id=media_id,
            media_title=metadata.get('title', f'Media {media_id}'),
            media_description=metadata.get('description'),
            media_duration=metadata.get('duration'),
            source=source,
            transcript=transcript[:500] + "..." if len(transcript) > 500 else transcript,
            summary=summary,
            script=script,
            translation=translation,
            target_language=target_language if translate else None,
            processing_time=round(processing_time, 2),
            style_used=style,
            model_used=self.ollama_client.default_model
        )