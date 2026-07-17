# 📹 Claude Vision Video Analyzer - Complete Specifications

## 🎯 What This Tool Does

This tool analyzes videos using AI to understand what's happening in them.

### Step-by-Step Process:
1. **INPUT**: You provide a video file (MP4, AVI, MOV, etc.)
2. **EXTRACTION**: FFmpeg splits video into image frames (every N seconds)
3. **ANALYSIS**: Claude AI looks at each frame and describes what it sees
4. **OUTPUT**: JSON file with frame-by-frame analysis

### Example Use Cases:
- **Sports Analysis** → Identify plays, athletes, key moments
- **Security Footage** → Detect suspicious activities, people
- **Medical Videos** → Identify procedures, instruments
- **Educational Content** → Extract key concepts, formulas from lectures
- **Meeting Recordings** → Summarize presentations, identify speakers
- **Quality Control** → Inspect products, find defects
- **Content Moderation** → Detect inappropriate content

---

## 💰 Cost Breakdown

### API Provider: Anthropic (Claude)
**Website**: https://console.anthropic.com/

### 🎁 Free Tier:
- ✅ **$5 USD in FREE credits** when you sign up
- Valid for 1 month
- No credit card required to start
- Perfect for testing this tool!

### 💵 Pricing (Vision API - Pay As You Go):

#### Claude 3.5 Sonnet (RECOMMENDED - Best Balance)
- Input: $3.00 per million tokens (~$0.003 per 1,000 tokens)
- Output: $15.00 per million tokens (~$0.015 per 1,000 tokens)

#### Claude 3 Opus (Highest Quality - Most Expensive)
- Input: $15.00 per million tokens (~$0.015 per 1,000 tokens)
- Output: $75.00 per million tokens (~$0.075 per 1,000 tokens)

#### Claude 3 Sonnet (Budget Option - Faster)
- Input: $3.00 per million tokens (~$0.003 per 1,000 tokens)
- Output: $15.00 per million tokens (~$0.015 per 1,000 tokens)

### 📊 Real Cost Examples (Using Claude 3.5 Sonnet):

**1 minute video** (30 frames at 2-second intervals):
- ~30 API calls
- **Cost: ~$0.50 - $1.50 USD**

**10 minute video** (300 frames):
- ~300 API calls
- **Cost: ~$5.00 - $15.00 USD**

**1 hour video** (1,800 frames):
- ~1,800 API calls
- **Cost: ~$30.00 - $90.00 USD**

💡 **TIP**: Increase `frame_interval` to reduce cost
- `interval=5` (every 5 seconds) = 60% less cost
- `interval=10` (every 10 seconds) = 80% less cost

### 💳 Billing:
- Charged per API request (per frame analyzed)
- Pay only for what you use (no monthly fees)
- Billed at the end of each month
- Can set spending limits in Anthropic console

---

## 🔑 How to Get & Add API Key

### Step 1: Get Your API Key

1. Go to: **https://console.anthropic.com/**

2. Click **"Sign Up"** (or "Sign In" if you have account)
   - Use your work email: `lokesh.neela@network.lilly.com`
   - Or any personal email

3. Verify your email

4. Navigate to **"API Keys"** in the left sidebar

5. Click **"Create Key"**
   - Give it a name like "Video Analyzer"

6. **Copy the API key** (looks like: `sk-ant-api03-xxx...`)
   - ⚠️ **IMPORTANT**: Save it now! You can't see it again later

7. (Optional) Add payment method to continue after free credits

### Step 2: Add API Key to the Project

#### METHOD 1: Using .env file (RECOMMENDED)

1. Navigate to project folder:
   ```bash
   cd claude-vision-video-analyzer
   ```

2. Copy the example config:
   ```bash
   copy .env.example .env
   ```

3. Open .env file in any text editor:
   ```bash
   notepad .env
   ```

4. Replace the placeholder with your actual key:
   ```
   Before: ANTHROPIC_API_KEY=your_api_key_here
   After:  ANTHROPIC_API_KEY=sk-ant-api03-xxxYOURKEYxxx
   ```

5. Save and close the file

✅ **Done!** The tool will automatically read this key

#### METHOD 2: Using Environment Variable (Alternative)

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-api03-xxxYOURKEYxxx"
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-api03-xxxYOURKEYxxx
```

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxYOURKEYxxx"
```

---

## 🚀 Complete End-to-End Usage (From Scratch)

### STEP 1: Install Prerequisites

#### Windows:

1. **Install Python 3.9+** from: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **Install FFmpeg:**
   
   **Option A: Chocolatey** (if you have it)
   ```bash
   choco install ffmpeg
   ```
   
   **Option B: Manual download**
   - Download from: https://ffmpeg.org/download.html
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to Windows PATH

3. **Verify installation:**
   ```bash
   python --version
   ffmpeg -version
   ```

### STEP 2: Download & Setup Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lokeshneela-1/claude-vision-video-analyzer.git
   ```

2. **Navigate to folder:**
   ```bash
   cd claude-vision-video-analyzer
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment:**
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

5. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - `anthropic` (Claude API)
   - `opencv-python` (video processing)
   - `ffmpeg-python` (frame extraction)
   - `python-dotenv` (config management)
   - `Pillow` (image processing)
   - `tqdm` (progress bars)

### STEP 3: Configure API Key

1. **Copy config template:**
   ```bash
   copy .env.example .env
   ```

2. **Edit .env file:**
   ```bash
   notepad .env
   ```

3. **Add your API key:**
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxYOURKEYxxx
   ```

4. **(Optional) Adjust settings:**
   ```
   FRAME_INTERVAL=2          # Extract frame every 2 seconds
   MODEL=claude-3-5-sonnet-20241022  # AI model to use
   OUTPUT_DIR=output_frames  # Where to save results
   ```

### STEP 4: Test Setup

1. **Run test script:**
   ```bash
   python test_setup.py
   ```

2. **You should see:**
   ```
   ✅ Python version OK
   ✅ FFmpeg installed
   ✅ All dependencies installed
   ✅ API key configured
   ✅ Connection to Claude API successful
   ```

If any ❌ appears, follow the error messages to fix

### STEP 5: Analyze Your First Video

**Basic analysis:**
```bash
python main.py --video path\to\your\video.mp4
```

**Custom interval (every 5 seconds):**
```bash
python main.py --video video.mp4 --interval 5
```

**Custom prompt:**
```bash
python main.py --video video.mp4 --prompt "Identify all people and objects"
```

**Save to specific folder:**
```bash
python main.py --video video.mp4 --output my_results
```

**Use different model:**
```bash
python main.py --video video.mp4 --model claude-3-opus-20240229
```

### STEP 6: View Results

After analysis completes, you'll find:

```
output_frames/
├── frames/                  # Extracted images
│   ├── frame_00001.jpg
│   ├── frame_00002.jpg
│   └── ...
└── analysis_TIMESTAMP.json  # AI analysis results
```

Open the JSON file to see:
- Frame-by-frame descriptions
- Objects identified
- Actions detected
- Text visible in frames
- Overall context

---

## 📊 Output Example

Sample JSON output structure:

```json
{
  "video_path": "sample.mp4",
  "total_frames_analyzed": 30,
  "frame_interval": 2.0,
  "model_used": "claude-3-5-sonnet-20241022",
  "analysis_timestamp": "2026-07-17T08:52:13",
  "frames": [
    {
      "frame_number": 1,
      "timestamp": "00:00:00",
      "frame_path": "output_frames/frames/frame_00001.jpg",
      "analysis": {
        "objects": ["person", "desk", "computer", "coffee mug"],
        "actions": "Person typing on keyboard",
        "setting": "Modern office environment",
        "text_visible": "Welcome to the presentation",
        "context": "Business presentation beginning"
      }
    },
    {
      "frame_number": 2,
      "timestamp": "00:00:02",
      "..."
    }
  ],
  "summary": "Video shows a business presentation..."
}
```

---

## 🎛️ Configuration Options

### Command Line Arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `--video PATH` | Path to video file (REQUIRED) | - |
| `--output DIR` | Output directory | `output_frames` |
| `--interval SECONDS` | Frame interval | `2.0` |
| `--model MODEL` | Claude model | `claude-3-5-sonnet-20241022` |
| `--prompt TEXT` | Custom analysis prompt | Default prompt |
| `--max-tokens NUM` | Max response tokens | `1024` |
| `--keep-frames` | Keep extracted frames | `false` |
| `--verbose` | Enable detailed logging | `false` |

### Environment Variables (.env file):

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Claude API key (REQUIRED) | - |
| `FRAME_INTERVAL` | Default frame interval | `2` |
| `OUTPUT_DIR` | Default output directory | `output_frames` |
| `MODEL` | Default Claude model | `claude-3-5-sonnet-20241022` |
| `MAX_TOKENS` | Default max tokens | `1024` |
| `KEEP_FRAMES` | Keep frames after analysis | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## 💡 Tips & Best Practices

### 💰 Cost Optimization:
- Start with `interval=5` or `interval=10` to reduce API calls
- Use Claude 3 Sonnet instead of Opus for faster/cheaper analysis
- Test on short video clips first ($0.50 vs $50)
- Set `MAX_TOKENS` lower (512) if you don't need detailed analysis

### ⚡ Performance:
- Keep `FRAME_INTERVAL` at 2+ seconds (smoother = slower/expensive)
- Process videos offline (not real-time)
- Expect ~2-5 seconds per frame analyzed

### 🎯 Quality:
- Use Claude 3.5 Sonnet for best balance
- Use Claude 3 Opus only for critical analysis
- Custom prompts improve accuracy for specific use cases
- Higher `MAX_TOKENS` = more detailed analysis but higher cost

### 🔒 Security:
- Never commit `.env` file to Git (already in `.gitignore`)
- Keep API key private
- Set spending limits in Anthropic console
- Use separate API keys for dev/production

---

## 📞 Support & Documentation

- **Repository**: https://github.com/Lokeshneela-1/claude-vision-video-analyzer
- **API Docs**: https://docs.anthropic.com/claude/docs/vision
- **Pricing**: https://www.anthropic.com/pricing
- **Console**: https://console.anthropic.com/

### Files to Read:
- `START_HERE.md` → Quick overview
- `README.md` → Main documentation
- `SETUP_GUIDE.md` → Detailed setup
- `END_TO_END_GUIDE.md` → Complete guide
- `examples/` → Usage examples

---

## 🏁 Quick Reference Card

### Minimum Cost Test:
```bash
# Test 10-second video clip with 5-second intervals
python main.py --video test.mp4 --interval 5
# Cost: ~$0.10 - $0.30
```

### Recommended Settings:
```bash
# Good balance of quality and cost
python main.py --video video.mp4 \
  --interval 2 \
  --model claude-3-5-sonnet-20241022 \
  --max-tokens 1024
```

### Budget Mode:
```bash
# Lower cost, still good quality
python main.py --video video.mp4 \
  --interval 10 \
  --model claude-3-sonnet-20240229 \
  --max-tokens 512
```

### Premium Mode:
```bash
# Best quality, higher cost
python main.py --video video.mp4 \
  --interval 1 \
  --model claude-3-opus-20240229 \
  --max-tokens 2048
```

---

## ✅ Summary

**What it does**: Analyzes videos frame-by-frame using AI

**Cost**: $5 free credits, then ~$0.50-$1.50 per minute of video

**API**: Claude Vision API from Anthropic

**Setup time**: 10-15 minutes

**Requirements**: Python 3.9+, FFmpeg, API key

**Output**: JSON file with detailed frame analysis

---

*Created by Lokesh Neela | Enterprise Edition | Powered by Claude AI*
