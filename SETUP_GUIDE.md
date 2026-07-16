# Complete Setup & Usage Guide for Claude Vision Video Analyzer

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Getting Claude API Key](#getting-claude-api-key)
4. [Running Your First Analysis](#running-your-first-analysis)
5. [Testing with Sample Video](#testing-with-sample-video)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Prerequisites

Before you begin, make sure you have:

- **Python 3.9 or higher**
  ```bash
  python --version
  ```

- **FFmpeg** installed
  
- **Claude API Key** (from Anthropic)

---

## Installation Steps

### Step 1: Install FFmpeg

**On macOS (using Homebrew):**
```bash
# Install Homebrew first if needed: https://brew.sh
brew install ffmpeg

# Verify installation
ffmpeg -version
```

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg

# Verify
ffmpeg -version
```

**On Windows:**

Option A - Using Chocolatey:
```powershell
choco install ffmpeg
```

Option B - Manual download:
1. Go to https://ffmpeg.org/download.html
2. Download the Windows build
3. Extract to a folder
4. Add the bin folder to your PATH

Verify:
```powershell
ffmpeg -version
```

---

### Step 2: Clone the Repository

```bash
git clone https://github.com/lokeshneela-1/claude-vision-video-analyzer.git
cd claude-vision-video-analyzer
```

---

### Step 3: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

---

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 5: Get Claude API Key

1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-`)
6. **Important**: Save it securely - you won't see it again!

---

### Step 6: Configure API Key

**Option A: Using .env file (Recommended)**

1. Copy the example config:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```bash
ANTHROPIC_API_KEY=sk-ant-your_key_here_xxxxx
FRAME_INTERVAL=2
OUTPUT_DIR=output_frames
```

3. Save the file

**Option B: Using Environment Variable**

**On macOS/Linux (bash/zsh):**
```bash
export ANTHROPIC_API_KEY=sk-ant-your_key_here_xxxxx
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your_key_here_xxxxx"
```

---

## Running Your First Analysis

### Test Setup

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Verify everything is working
python main.py --help
```

### Analyze a Video

```bash
# Basic usage
python main.py --video your_video.mp4

# With custom output directory
python main.py --video your_video.mp4 --output my_results

# Extract fewer frames (every 5 seconds)
python main.py --video your_video.mp4 --interval 5

# Custom analysis prompt
python main.py --video your_video.mp4 --prompt "Identify any people and describe their actions"
```

---

## Testing with Sample Video

### Create a Test Video

If you don't have a video file, create one:

```bash
# Create 10-second test video
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 \
        -f lavfi -i sine=f=1000:d=10 \
        -pix_fmt yuv420p \
        test_video.mp4

# Run analyzer on test video
python main.py --video test_video.mp4 --interval 5
```

### Download Sample Video

Or download a free sample video:

```bash
# Example: Download a short clip
wget https://commondatastorage.googleapis.com/gtv-videos-library/sample/BigBuckBunny.mp4 -O sample.mp4

# Analyze it
python main.py --video sample.mp4
```

---

## Results

After analysis completes, check the output:

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

### View Results

**JSON Results (for processing):**
```bash
cat output_frames/video_name/analysis_results.json
```

**Summary (for humans):**
```bash
cat output_frames/video_name/summary.txt
```

---

## Troubleshooting

### Issue: "FFmpeg not found"

**Solution:**
```bash
# Verify FFmpeg is installed
ffmpeg -version

# If not, install it:
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
# Windows: choco install ffmpeg
```

### Issue: "ANTHROPIC_API_KEY not found"

**Solutions:**

1. Check `.env` file exists:
```bash
ls -la .env  # macOS/Linux
dir .env    # Windows
```

2. Verify key is set:
```bash
# macOS/Linux
echo $ANTHROPIC_API_KEY

# Windows PowerShell
$env:ANTHROPIC_API_KEY
```

3. Make sure `.env` is in the project root:
```bash
pwd  # Should show project directory
ls   # Should list .env file
```

### Issue: "Video file not found"

**Solution:**
```bash
# Use absolute path
python main.py --video /full/path/to/video.mp4

# Or copy video to project directory
cp /path/to/video.mp4 ./
python main.py --video video.mp4
```

### Issue: "Could not extract frames"

**Solutions:**

1. Verify video file:
```bash
ffprobe video.mp4
```

2. Check file format:
```bash
# FFmpeg should recognize the format
ffmpeg -i video.mp4
```

3. Try converting video:
```bash
ffmpeg -i old_video.avi -c:v libx264 -c:a aac new_video.mp4
python main.py --video new_video.mp4
```

### Issue: API Rate Limit Exceeded

**Solution:**
- Wait a few minutes before running analysis
- Use a longer frame interval: `--interval 5` or higher
- Reduce video size/length

### Issue: High API Costs

**Solution:**
- Increase frame interval: `--interval 10` (fewer frames = fewer API calls)
- Use faster model: `--model claude-3-5-sonnet-20241022`
- Process shorter videos
- Use `--max-frames 100` to limit frame count

---

## Advanced Usage

### Custom Analysis Prompts

```bash
# Security/Surveillance
python main.py --video security.mp4 \
  --prompt "Identify any suspicious activities or people of interest"

# Sports Analysis
python main.py --video game.mp4 \
  --interval 0.5 \
  --prompt "Identify plays, athletes, and significant moments"

# Educational Content
python main.py --video lecture.mp4 \
  --prompt "Extract key concepts, formulas, equations, and main teaching points"

# Medical/Scientific
python main.py --video procedure.mp4 \
  --prompt "Document the steps, tools used, and key observations"
```

### Different Claude Models

```bash
# Fast & affordable (recommended for most uses)
python main.py --video video.mp4 --model claude-3-5-sonnet-20241022

# Most powerful but slower
python main.py --video video.mp4 --model claude-3-opus-20240229

# Balanced option
python main.py --video video.mp4 --model claude-3-sonnet-20240229
```

### Batch Processing

Process multiple videos:

```bash
#!/bin/bash
for video in videos/*.mp4; do
  echo "Processing: $video"
  python main.py --video "$video" --output "output_$(basename $video .mp4)"
  echo "Done: $video\n"
done
```

### Reanalyze with Different Prompt

If frames already extracted:

```bash
# Analyze existing frames with new prompt
python main.py --skip-extract \
  --prompt "Look for anything unusual"
```

---

## API Cost Estimation

**Typical costs per video:**

| Video Length | Frame Interval | Est. Frames | Est. Cost* |
|-------------|----------------|-------------|-----------|
| 1 min       | 2s             | 30          | $0.07     |
| 5 min       | 2s             | 150         | $0.36     |
| 10 min      | 2s             | 300         | $0.72     |
| 10 min      | 5s             | 120         | $0.29     |
| 1 hour      | 10s            | 360         | $0.86     |

*Estimates based on Claude 3.5 Sonnet pricing (~$0.003 per image)

---

## Next Steps

1. **Create a wrapper script** for your workflow
2. **Integrate with your application** using the Python API
3. **Set up batch processing** for multiple videos
4. **Export results** to your database or CMS

---

## Getting Help

- Check existing issues: https://github.com/lokeshneela-1/claude-vision-video-analyzer/issues
- Check Claude API docs: https://docs.anthropic.com
- Create a new issue with:
  - Video info (format, size, length)
  - Error message
  - Steps to reproduce
  - Your OS and Python version

---

## Important Notes

⚠️ **API Key Safety:**
- Never commit `.env` to git
- Never share your API key
- Use environment variables in production
- Rotate keys regularly

⚠️ **Cost Management:**
- Monitor API usage in dashboard
- Use appropriate frame intervals
- Test with small videos first
- Set spending limits in Anthropic console

⚠️ **Privacy:**
- Don't process sensitive/private videos without safeguards
- Consider where results are stored
- Implement access controls for results

---

## License

MIT License - See LICENSE file

**Happy video analyzing! 🎉**
