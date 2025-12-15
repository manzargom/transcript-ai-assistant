from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime

from app.core.assistant import YouTubeAIAssistant, ProcessingResult
from app.api.endpoints import api_bp
from app.routes import main_bp
from app.models import ProcessingRequest


def create_app(config_name='default'):
    """Application factory."""
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config.from_object(f'config.{config_name}')
    
    # Ensure directories exist
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize assistant
    assistant = YouTubeAIAssistant(
        ollama_url=app.config.get('OLLAMA_URL', 'http://localhost:11434'),
        default_model=app.config.get('DEFAULT_MODEL', 'mistral:7b-instruct-q4_K_M')
    )
    app.config['ASSISTANT'] = assistant
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)