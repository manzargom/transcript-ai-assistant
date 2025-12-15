# Transcript-AI Assistant

A generic Flask application that processes media transcripts using local Ollama AI. 
Extract transcripts from various sources, generate summaries, create new scripts, 
and translate content - all powered by your local AI models.

## Why "Transcript-AI Assistant"?

The name reflects the true purpose: **Transcript** (working with text from media) + 
**AI** (powered by local Ollama) + **Assistant** (helps creators with content).

## Features

- 📝 **Multi-source Transcripts**: Currently supports YouTube (expandable to Vimeo, podcasts, audio files)
- 🤖 **Local AI Processing**: Uses your Ollama models - no API costs, full privacy
- 📊 **Smart Analysis**: Generate summaries, create scripts in different styles
- 🌐 **Translation**: Optional translation to Spanish or other languages
- 🔌 **REST API**: Full API for integration with other creator tools
- 🎨 **Clean Web Interface**: User-friendly interface for manual processing

## Quick Start

1. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate