# Claude Vision Video Analyzer

A production-ready Python tool that extracts frames from videos and analyzes them using Claude's Vision API. This replaces the Ollama-based approach with superior AI analysis, better context understanding, and no local model setup required.

## ✨ Features

- 🎞️ **Frame Extraction** – Extract frames from any video using FFmpeg
- 🤖 **Claude Vision Analysis** – Powerful AI-powered image understanding
- 📊 **Structured Output** – JSON results with frame-by-frame analysis
- ⚡ **Batch Processing** – Handle multiple frames efficiently
- 🎨 **Progress Tracking** – Real-time progress with visual indicators
- 📝 **Detailed Logging** – Comprehensive logs for debugging
- 🔧 **Configurable** – Custom intervals, models, and prompts

## 📋 Requirements

- Python 3.9+
- FFmpeg (for frame extraction)
- Claude API key (from Anthropic)

## 🚀 Quick Start

### Step 1: Install FFmpeg

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

### Step 2: Clone & Setup

```bash
git clone https://github.com/lokeshneela-1/claude-vision-video-analyzer.git
cd claude-vision-video-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure API Key

Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_api_key_here
FRAME_INTERVAL=2  # Extract frame every 2 seconds (optional)
OUTPUT_DIR=output_frames  # Output directory (optional)
```

### Step 4: Run Analysis

```bash
python main.py --video path/to/your/video.mp4
```

## 📖 Detailed Usage

### Basic Usage

```bash
# Analyze a video with default settings
python main.py --video sample.mp4

# Specify custom output directory
python main.py --video sample.mp4 --output my_results

# Extract frames every 5 seconds instead of default 2
python main.py --video sample.mp4 --interval 5

# Use different Claude model (default: claude-3-5-sonnet-20241022)
python main.py --video sample.mp4 --model claude-3-opus-20240229
```

### Advanced Options

```bash
# Custom analysis prompt
python main.py --video sample.mp4 --prompt "Describe what people are doing in each frame"

# Skip frame extraction (reuse existing frames)
python main.py --video sample.mp4 --skip-extract

# Show help
python main.py --help
```

## 📁 Output Structure

```
output_frames/
├── video_name/
│   ├── frames/
│   │   ├── frame_0001.jpg
│   │   ├── frame_0002.jpg
│   │   └── ...
│   ├── analysis_results.json
│   ├── summary.txt
│   └── metadata.json
```

### analysis_results.json

```json
{
  "video_path": "path/to/video.mp4",
  "total_frames": 150,
  "analysis_date": "2024-01-15T10:30:00",
  "frames": [
    {
      "frame_number": 1,
      "timestamp": "0:00:00",
      "frame_file": "frame_0001.jpg",
      "analysis": "A person sitting at a desk working on a laptop..."
    },
    {
      "frame_number": 2,
      "timestamp": "0:00:02",
      "frame_file": "frame_0002.jpg",
      "analysis": "Close-up of the laptop screen showing code..."
    }
  ]
}
```

## 🎯 Common Use Cases

### 1. Content Analysis
```bash
python main.py --video interview.mp4 --prompt "Identify key topics being discussed and who is speaking"
```

### 2. Security/Surveillance
```bash
python main.py --video surveillance.mp4 --prompt "Describe any unusual activities or events"
```

### 3. Sports Analysis
```bash
python main.py --video game.mp4 --interval 0.5 --prompt "Identify plays, athletes, and significant moments"
```

### 4. Educational Content
```bash
python main.py --video lecture.mp4 --prompt "Extract key concepts, formulas, and main points discussed"
```

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_API_URL=https://api.anthropic.com  # Optional

# Frame Extraction
FRAME_INTERVAL=2  # Seconds between frames
VIDEO_PATH=./videos  # Default input directory

# Output
OUTPUT_DIR=output_frames
KEEP_FRAMES=true  # Keep extracted frames after analysis

# Claude Configuration
MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=1024
TEMPERATURE=0.7
```

## 📊 Supported Video Formats

- MP4, MKV, AVI, MOV, WebM
- Most formats supported by FFmpeg

## 🛠️ Troubleshooting

### FFmpeg not found
```bash
# Verify FFmpeg is installed
ffmpeg -version

# If not installed, follow installation steps above
```

### API Key Issues
```
Error: ANTHROPIC_API_KEY not found

Solution:
1. Create .env file in project root
2. Add: ANTHROPIC_API_KEY=your_key_here
3. Run: python main.py --video video.mp4
```

### Video Not Processing
```
Error: Could not extract frames

Solutions:
- Verify video file exists: ls -la video.mp4
- Check file format is supported by FFmpeg
- Try: ffmpeg -i video.mp4 (should show video info)
```

### Slow Processing
- Increase FRAME_INTERVAL to skip more frames
- Use a smaller video file for testing
- Check Claude API rate limits

## 📊 Performance Tips

- **Reduce frame count**: Increase `--interval` to skip more frames
- **Faster processing**: Use `claude-3-5-sonnet-20241022` (faster than Opus)
- **Batch processing**: Process multiple videos in sequence
- **Skip re-extraction**: Use `--skip-extract` flag

## 🧪 Testing

### Test with Sample Video

```bash
# Create a test video (if you don't have one)
# Using ffmpeg to generate a test video
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -f lavfi -i sine=f=1000:d=10 test_video.mp4

# Run analyzer
python main.py --video test_video.mp4
```

### Quick Test (5 frames)

```bash
python main.py --video sample.mp4 --interval 10 --output test_output
```

## 📝 Example Output

```json
{
  "video_path": "sample.mp4",
  "total_frames": 10,
  "processing_time_seconds": 23.45,
  "frames": [
    {
      "frame_number": 1,
      "timestamp": "0:00:00",
      "frame_file": "frame_0001.jpg",
      "analysis": "A bright blue background with no objects visible. Clean, minimalist aesthetic with natural lighting."
    }
  ]
}
```

## 🚀 Advanced Features

### Running as a Web Service (Coming Soon)
```bash
python app.py  # Start Flask/FastAPI server
# POST /api/analyze with video file
```

### Batch Processing

```bash
# Process all MP4 files in a directory
for video in videos/*.mp4; do
  python main.py --video "$video"
done
```

## 📚 API Reference

### Main Functions

#### `VideoAnalyzer()`
Main class for video analysis.

```python
from analyzer import VideoAnalyzer

analyzer = VideoAnalyzer(
    api_key="your-key",
    model="claude-3-5-sonnet-20241022",
    frame_interval=2
)

results = analyzer.analyze("video.mp4")
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🎓 Learning Resources

- [Claude API Documentation](https://docs.anthropic.com)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Video Processing Guide](https://docs.anthropic.com/en/docs/guides/vision)

## ⚠️ Important Notes

- **API Costs**: Each image analysis uses Claude API tokens. Monitor usage.
- **Video Quality**: Higher resolution videos = better analysis but more tokens
- **Rate Limits**: Anthropic API has rate limits. Adjust processing speed accordingly
- **Privacy**: Don't process sensitive videos without proper safeguards

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with:
   - Video format and size
   - Error message
   - Steps to reproduce
   - System info (OS, Python version)

## 🎉 Examples

Check the `examples/` directory for:
- [x] Basic video analysis
- [x] Custom prompt analysis
- [x] Batch processing
- [x] Integration with Python scripts

---

**Built with ❤️ using Claude API and Python**
