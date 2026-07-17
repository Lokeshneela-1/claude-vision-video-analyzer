"""
Flask Web Application for Claude Video Analyzer
Enterprise UI/UX with Eli Lilly design
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import json
import os
from pathlib import Path
from datetime import datetime
import io
import hashlib

from analyzer import VideoAnalyzer
from utils import print_info, print_error, print_success
from video_index import VideoIndex
from chatbot import VideoChatbot

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output_frames'

# Create folders if they don't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Initialize video index and chatbot
print_info("Initializing Video Index and Chatbot...")
video_index = VideoIndex()
chatbot = VideoChatbot(video_index)
print_success("✅ Chatbot ready!")

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_video_id(filename):
    """Generate unique ID for video based on filename and timestamp"""
    unique_str = f"{filename}_{datetime.now().isoformat()}"
    return hashlib.md5(unique_str.encode()).hexdigest()[:16]

@app.route('/')
def index():
    """Serve the web UI"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Handle video upload and analysis"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: MP4, AVI, MOV, etc.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        saved_filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)
        
        print_info(f"Video uploaded: {saved_filename}")
        
        # Get parameters
        frame_interval = float(request.form.get('frame_interval', 2))
        custom_prompt = request.form.get('custom_prompt', '')
        max_frames = request.form.get('max_frames', None)
        if max_frames:
            max_frames = int(max_frames)
        
        # Analyze video
        try:
            analyzer = VideoAnalyzer(
                output_dir=app.config['OUTPUT_FOLDER'],
                frame_interval=frame_interval,
                verbose=True
            )
            
            print_info(f"Starting analysis of {filename}...")
            results = analyzer.analyze(
                video_path=filepath,
                custom_prompt=custom_prompt if custom_prompt else None,
                max_frames=max_frames
            )
            
            print_success(f"Analysis complete: {filename}")
            
            # Generate video ID and index the analysis for chatbot
            video_id = generate_video_id(saved_filename)
            try:
                print_info("Indexing video analysis for chatbot...")
                video_index.index_video_analysis(
                    video_id=video_id,
                    video_path=filepath,
                    analysis_results=results
                )
                print_success("✅ Video indexed for Q&A!")
            except Exception as idx_error:
                print_error(f"Warning: Failed to index video: {idx_error}")
            
            return jsonify({
                'success': True,
                'results': results,
                'video_id': video_id,  # Return video_id for chatbot
                'message': 'Video analysis completed successfully'
            }), 200
            
        except Exception as e:
            print_error(f"Analysis failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Analysis failed: {str(e)}'
            }), 500
            
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Upload error: {str(e)}'
        }), 500

@app.route('/api/results/<video_name>', methods=['GET'])
def get_results(video_name):
    """Get analysis results for a video"""
    try:
        results_file = Path(app.config['OUTPUT_FOLDER']) / video_name / 'analysis_results.json'
        
        if not results_file.exists():
            return jsonify({'error': 'Results not found'}), 404
        
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<video_name>', methods=['GET'])
def download_results(video_name):
    """Download results as JSON"""
    try:
        results_file = Path(app.config['OUTPUT_FOLDER']) / video_name / 'analysis_results.json'
        
        if not results_file.exists():
            return jsonify({'error': 'Results not found'}), 404
        
        return send_file(
            str(results_file),
            as_attachment=True,
            download_name=f'{video_name}_analysis_results.json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========================================
# CHATBOT ENDPOINTS ⭐ NEW
# ========================================

@app.route('/api/chat', methods=['POST'])
def chat_with_video():
    """Chat with analyzed video"""
    try:
        data = request.json
        video_id = data.get('video_id')
        question = data.get('question')
        
        if not video_id or not question:
            return jsonify({'error': 'video_id and question are required'}), 400
        
        # Get answer from chatbot
        result = chatbot.answer_question(video_id, question)
        
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'timestamps': result['timestamps'],
            'frames': result['frames'],
            'confidence': result['confidence'],
            'relevant_frames': result.get('relevant_frames', [])
        }), 200
        
    except Exception as e:
        print_error(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summary/<video_id>', methods=['GET'])
def get_video_summary(video_id):
    """Get AI-generated summary of video"""
    try:
        summary = chatbot.get_video_summary(video_id)
        return jsonify({
            'success': True,
            'summary': summary,
            'video_id': video_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/suggestions/<video_id>', methods=['GET'])
def get_suggested_questions(video_id):
    """Get suggested questions for video"""
    try:
        suggestions = chatbot.suggest_questions(video_id)
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'video_id': video_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversation/<video_id>', methods=['GET'])
def get_conversation(video_id):
    """Get conversation history for video"""
    try:
        conversation = chatbot.memory.get_conversation(video_id)
        return jsonify({
            'success': True,
            'conversation': conversation,
            'video_id': video_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export-conversation/<video_id>', methods=['GET'])
def export_conversation(video_id):
    """Export conversation to text file"""
    try:
        filepath = chatbot.export_conversation(video_id)
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f'conversation_{video_id}.txt'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/videos', methods=['GET'])
def list_videos():
    """List all indexed videos"""
    try:
        video_ids = video_index.list_indexed_videos()
        return jsonify({
            'success': True,
            'videos': video_ids,
            'count': len(video_ids)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# END CHATBOT ENDPOINTS
# ========================================

@app.route('/api/status', methods=['GET'])
def status():
    """Health check endpoint"""
    try:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        has_api_key = bool(api_key)
        
        return jsonify({
            'status': 'healthy',
            'service': 'Claude Video Analyzer',
            'version': '1.0.0',
            'api_configured': has_api_key,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large. Maximum size: 500MB'
    }), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Video Analyzer Web UI')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1, use 0.0.0.0 for network access)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    print_info("=" * 70)
    print_info("Claude Video Analyzer - Web Application")
    print_info("Eli Lilly Enterprise Edition")
    print_info("=" * 70)
    print_info(f"Starting server on {args.host}:{args.port}...")
    print_info("")
    print_info("Access the application at:")
    print_info(f"  • Local:   http://localhost:{args.port}")
    if args.host == '0.0.0.0':
        print_info(f"  • Network: http://YOUR_IP_ADDRESS:{args.port}")
    print_info("")
    print_info("Press CTRL+C to stop the server")
    print_info("=" * 70)
    
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        threaded=True
    )
