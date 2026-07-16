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

from analyzer import VideoAnalyzer
from utils import print_info, print_error, print_success

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output_frames'

# Create folders if they don't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            
            return jsonify({
                'success': True,
                'results': results,
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
    print_info("Starting Claude Video Analyzer Web UI...")
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False,
        threaded=True
    )
