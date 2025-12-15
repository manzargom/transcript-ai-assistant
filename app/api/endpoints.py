from flask import Blueprint, request, jsonify, current_app
import json
from datetime import datetime
import uuid

from app.models import ProcessingRequest, APIResponse
from app.core.assistant import ProcessingResult

api_bp = Blueprint('api', __name__)


@api_bp.route('/process', methods=['POST'])
def process_video():
    """API endpoint for video processing."""
    data = request.get_json()
    
    # Validate request
    if not data or 'video_url' not in data:
        return jsonify({
            'error': 'Missing video_url parameter',
            'status': 'error'
        }), 400
    
    try:
        assistant = current_app.config['ASSISTANT']
        
        # Process video
        result = assistant.process_video(
            video_input=data['video_url'],
            style=data.get('style', 'educational'),
            translate=data.get('translate', False),
            language=data.get('language', 'es')
        )
        
        # Prepare response
        response_data = {
            'request_id': str(uuid.uuid4()),
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'data': result.to_dict(),
            'api_version': '1.0'
        }
        
        # Save to file if requested
        if data.get('save_output', False):
            filename = f"outputs/api_result_{result.video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@api_bp.route('/status', methods=['GET'])
def api_status():
    """Check API and Ollama status."""
    try:
        assistant = current_app.config['ASSISTANT']
        
        # Test Ollama connection
        ollama_status = assistant.ollama_client.check_connection()
        
        return jsonify({
            'status': 'online',
            'ollama_connected': ollama_status,
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'process_video': '/api/v1/process',
                'metadata': '/api/v1/metadata',
                'health': '/api/v1/health'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@api_bp.route('/metadata/<video_id>', methods=['GET'])
def get_metadata(video_id):
    """Get video metadata only."""
    try:
        assistant = current_app.config['ASSISTANT']
        metadata = assistant.extract_metadata(video_id)
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'metadata': metadata,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'youtube-ai-assistant',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@api_bp.route('/models', methods=['GET'])
def list_models():
    """List available Ollama models."""
    try:
        assistant = current_app.config['ASSISTANT']
        models = assistant.ollama_client.list_models()
        
        return jsonify({
            'status': 'success',
            'models': models,
            'default_model': assistant.ollama_client.default_model,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500