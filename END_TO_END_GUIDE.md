# Complete End-to-End Implementation Guide
## Claude Vision Video Analyzer

This guide takes you through every step to get the video analyzer working from zero to production.

---

## 📚 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Complete Setup (Step-by-Step)](#complete-setup-step-by-step)
4. [First Run & Testing](#first-run--testing)
5. [Understanding the Output](#understanding-the-output)
6. [Integration Guide](#integration-guide)
7. [Production Deployment](#production-deployment)
8. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Project Overview

**What This Does:**
- Extracts frames from any video file (MP4, AVI, MOV, etc.)
- Sends each frame to Claude's Vision API for analysis
- Returns structured JSON with detailed frame-by-frame analysis
- Handles batch processing of multiple videos
- Provides beautiful CLI interface with progress tracking

**Key Differences from Original (Ollama-based):**

| Feature | Original (Ollama) | This Version (Claude) |
|---------|------------------|----------------------|
| Setup   | Complex (local model) | Simple (API-based) |
| Speed   | Slow (limited by hardware) | Fast (Claude infrastructure) |
| Quality | Good | Excellent |
| Cost    | Free but hardware-intensive | Pay per use (~$0.003/image) |
| Scalability | Limited to local machine | Unlimited |
| Maintenance | Manage local models | Zero maintenance |

---

## Architecture

```
┌─────────────────────┐
│   Video File        │
│  (MP4/AVI/MOV)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   FFmpeg            │
│   (Frame Extract)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Frame Images      │
│   (JPEG/PNG)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Claude Vision API │
│   (Analysis)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Analysis Results  │
│   (JSON)            │
└─────────────────────┘
```

---

## Complete Setup (Step-by-Step)

### Prerequisites Checklist

Before starting, make sure you have:
- [ ] Computer with internet connection
- [ ] GitHub account (optional, for cloning)
- [ ] Anthropic account (required, free)
- [ ] 15 minutes of time

### Step 1: Install System Dependencies

#### On macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.9+
brew install python@3.11

# Install FFmpeg
brew install ffmpeg

# Verify installations
python3 --version
ffmpeg -version
```

#### On Ubuntu/Debian

```bash
# Update package manager
sudo apt-get update

# Install Python 3.9+
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# Install FFmpeg
sudo apt-get install ffmpeg

# Verify installations
python3.11 --version
ffmpeg -version
```

#### On Windows

**Option A: Using Chocolatey (Easiest)**

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python

# Install FFmpeg
choco install ffmpeg

# Restart PowerShell and verify
python --version
ffmpeg -version
```

**Option B: Manual Installation**

1. **Python:** Download from https://www.python.org/downloads/
   - Download Python 3.11+
   - Run installer
   - ✓ Check "Add Python to PATH"

2. **FFmpeg:**
   - Download from https://ffmpeg.org/download.html
   - Extract to folder
   - Add to PATH or use full path

3. **Verify in PowerShell:**
```powershell
python --version
ffmpeg -version
```

---

### Step 2: Get Claude API Key

1. Go to https://console.anthropic.com/
2. Click **Sign Up** (if needed) or **Sign In**
3. Navigate to **API Keys** in the left sidebar
4. Click **Create Key**
5. Name it (e.g., "Video Analyzer")
6. **Copy the key** (starts with `sk-ant-`)
7. **Save it somewhere secure** - you won't see it again!

**Example key format:**
```
sk-ant-v0-abc123def456...xyz789
```

---

### Step 3: Clone or Download the Project

**Option A: Using Git (Recommended)**

```bash
# Clone the repository
git clone https://github.com/lokeshneela-1/claude-vision-video-analyzer.git

# Navigate to project
cd claude-vision-video-analyzer
```

**Option B: Manual Download**

1. Go to https://github.com/lokeshneela-1/claude-vision-video-analyzer
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file
4. Open Terminal/PowerShell in that folder

---

### Step 4: Create Python Virtual Environment

**On macOS/Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) at the start of your terminal
```

**On Windows (PowerShell):**

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1

# If you get permission error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# You should see (venv) at the start of your terminal
```

**On Windows (Command Prompt):**

```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat

# You should see (venv) at the start
```

---

### Step 5: Install Python Dependencies

```bash
# Make sure virtual environment is active (you should see (venv))

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# This may take 1-2 minutes
```

---

### Step 6: Configure API Key

**Create `.env` file with your API key:**

**On macOS/Linux:**

```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_key_here
FRAME_INTERVAL=2
OUTPUT_DIR=output_frames
MODEL=claude-3-5-sonnet-20241022
EOF

# Replace your_key_here with your actual key
```

**Or edit manually:**

```bash
# Open in text editor
nano .env
# or
vim .env
```

**On Windows:**

Create a file named `.env` with this content:

```env
ANTHROPIC_API_KEY=your_key_here
FRAME_INTERVAL=2
OUTPUT_DIR=output_frames
MODEL=claude-3-5-sonnet-20241022
```

**Example `.env` file:**

```env
# Paste your actual key from step 2
ANTHROPIC_API_KEY=sk-ant-v0-abc123def456ghi789jklm
FRAME_INTERVAL=2
OUTPUT_DIR=output_frames
```

⚠️ **Important:** Don't commit `.env` to git - it's in `.gitignore` for security!

---

### Step 7: Test Your Setup

```bash
# Make sure venv is active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run setup test
python test_setup.py
```

You should see:
```
============================================================
  Claude Vision Video Analyzer - Setup Verification
============================================================

✓ Python version: 3.11.x
✓ FFmpeg installed: ffmpeg version N-xxxxx
✓ FFprobe installed: ffprobe version N-xxxxx
✓ Python Packages: ALL PASS
✓ API Key Configuration: API key found
✓ Module Imports: analyzer module imported successfully
...

Summary
Checks passed: 8/8

✓ All checks passed! You're ready to use Claude Vision Video Analyzer
```

If any check fails, see [FAQ & Troubleshooting](#faq--troubleshooting)

---

## First Run & Testing

### Test 1: Create a Test Video

```bash
# Generate a 5-second test video
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=5 \
        -f lavfi -i sine=f=1000:d=5 \
        -pix_fmt yuv420p \
        test_video.mp4
```

Expected output:
```
test_video.mp4 should appear in current directory
```

### Test 2: Run First Analysis

```bash
# Make sure venv is active
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Analyze the test video
python main.py --video test_video.mp4
```

Expected output:
```
============================================================
  Claude Vision Video Analyzer
============================================================

ℹ️  Starting video analysis...
ℹ️  Video: test_video.mp4
ℹ️  Output: output_frames
ℹ️  Frame interval: 2.0s
ℹ️  Model: claude-3-5-sonnet-20241022

Extracting frames at 2.0s intervals...
✓ Extracted 3 frames

Analyzing frames with Claude...
  [1/3] Analyzing frame_0001.jpg... ✓
  [2/3] Analyzing frame_0002.jpg... ✓
  [3/3] Analyzing frame_0003.jpg... ✓

✓ Analysis complete!
Total frames processed: 3
Processing time: X.XXs
Output saved to: output_frames/test_video

First frame analysis sample:
  Frame: frame_0001.jpg
  Timestamp: 0:00:00
  Analysis: A solid blue background with uniform coloring...

Results saved to: output_frames/test_video/analysis_results.json
```

### Test 3: View Results

```bash
# View the analysis results
cat output_frames/test_video/analysis_results.json

# Or view the summary
cat output_frames/test_video/summary.txt
```

---

## Understanding the Output

### Output Directory Structure

```
output_frames/
├── test_video/                    # Video name directory
│   ├── frames/                    # Extracted frame images
│   │   ├── frame_0001.jpg
│   │   ├── frame_0002.jpg
│   │   ├── frame_0003.jpg
│   │   └── ...
│   ├── analysis_results.json      # Main results (JSON)
│   ├── summary.txt                # Human-readable summary
│   └── metadata.json              # Video metadata
```

### Analyzing Results

**JSON Structure:**

```json
{
  "video_path": "test_video.mp4",
  "video_duration": 5.0,
  "total_frames": 3,
  "frames_analyzed": 3,
  "frame_interval": 2.0,
  "model": "claude-3-5-sonnet-20241022",
  "processing_time_seconds": 12.34,
  "frames": [
    {
      "frame_number": 1,
      "timestamp": "0:00:00",
      "frame_file": "frame_0001.jpg",
      "analysis": "A solid blue background with uniform coloring..."
    }
  ]
}
```

### Processing Results with Python

```python
import json

# Load results
with open("output_frames/test_video/analysis_results.json") as f:
    results = json.load(f)

# Access data
for frame in results['frames']:
    print(f"Frame {frame['frame_number']} ({frame['timestamp']})")
    print(f"Analysis: {frame['analysis']}\n")
```

---

## Integration Guide

### Using as Python Module

```python
from analyzer import VideoAnalyzer

# Create analyzer
analyzer = VideoAnalyzer(
    output_dir="my_results",
    frame_interval=3.0,
    model="claude-3-5-sonnet-20241022"
)

# Analyze video
results = analyzer.analyze(video_path="my_video.mp4")

# Process results
for frame in results['frames']:
    print(f"{frame['timestamp']}: {frame['analysis']}")
```

### Using CLI with Custom Scripts

```bash
#!/bin/bash
# process_videos.sh

for video in *.mp4; do
    echo "Processing: $video"
    python main.py --video "$video" --interval 5
    echo "Done: $video"
done
```

### Docker Integration

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run analyzer
ENTRYPOINT ["python", "main.py"]
```

Build and run:

```bash
docker build -t video-analyzer .
docker run -v $(pwd):/data video-analyzer --video /data/sample.mp4
```

---

## Production Deployment

### 1. Environment Configuration

Create `.env.production`:

```env
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}  # Set via environment variable
FRAME_INTERVAL=5
OUTPUT_DIR=/var/output/frames
MODEL=claude-3-5-sonnet-20241022
LOG_LEVEL=INFO
```

### 2. Error Handling

```python
import logging
from analyzer import VideoAnalyzer

logger = logging.getLogger(__name__)

try:
    analyzer = VideoAnalyzer()
    results = analyzer.analyze("video.mp4")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
except RuntimeError as e:
    logger.error(f"Processing error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### 3. Rate Limiting

```python
from time import sleep

videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    analyzer.analyze(video)
    sleep(5)  # Wait 5 seconds between videos to avoid rate limits
```

### 4. Monitoring

```python
import json
from pathlib import Path

# Track processing
logs = []

for video in videos:
    try:
        results = analyzer.analyze(video)
        logs.append({
            "video": video,
            "status": "success",
            "frames": len(results['frames']),
            "time": results['processing_time_seconds']
        })
    except Exception as e:
        logs.append({
            "video": video,
            "status": "failed",
            "error": str(e)
        })

# Save logs
with open("processing_log.json", "w") as f:
    json.dump(logs, f, indent=2)
```

---

## FAQ & Troubleshooting

### Q: "FFmpeg not found"

**A:** FFmpeg is not installed or not in PATH.

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg

# Verify
ffmpeg -version
```

### Q: "ANTHROPIC_API_KEY not found"

**A:** API key not configured properly.

Check:
1. `.env` file exists in project root
2. Key is set: `ANTHROPIC_API_KEY=sk-ant-...`
3. File is saved
4. Not wrapped in quotes

### Q: "Video file not found"

**A:** Wrong video path.

```bash
# Use absolute path
python main.py --video /full/path/to/video.mp4

# Or copy video to project directory
cp /path/to/video.mp4 ./
python main.py --video video.mp4
```

### Q: "API rate limit exceeded"

**A:** Too many requests too fast.

Solutions:
- Increase interval between videos: `sleep(60)`
- Increase frame interval: `--interval 10`
- Use `--max-frames 50`
- Wait 60 seconds before retrying

### Q: "High API costs"

**A:** Analyzing too many frames.

Cost reduction:
- Increase `--interval 5` (extract fewer frames)
- Use `--max-frames 100` (limit frames)
- Use faster model: `--model claude-3-5-sonnet-20241022`
- Only analyze short videos

### Q: "Permission denied" on Linux

**A:** Virtual environment issue.

```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Q: "Module not found" error

**A:** Dependencies not installed or venv not active.

```bash
# Check venv is active (should see (venv))
which python
# or on Windows
Get-Command python

# If not active, activate:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

---

## Next Steps

1. **Test with your own video:**
   ```bash
   python main.py --video your_video.mp4
   ```

2. **Try custom prompts:**
   ```bash
   python main.py --video video.mp4 \
     --prompt "Describe any people and their activities"
   ```

3. **Batch process multiple videos:**
   ```bash
   python examples/03_batch_processing.py
   ```

4. **Integrate into your application:**
   - See `examples/` directory
   - Read `analyzer.py` for API reference

5. **Monitor costs:**
   - Check Anthropic dashboard
   - Set spending limits

---

## Support

- **Documentation:** See README.md
- **Examples:** Check `examples/` directory
- **Issues:** Create GitHub issue with:
  - Video info (format, size, length)
  - Error message
  - Steps to reproduce
  - OS and Python version

---

**You're all set! Happy analyzing! 🎉**
