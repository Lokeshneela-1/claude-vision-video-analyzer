# 🚀 Complete Workflow Guide - End to End

## 📋 Overview

This guide shows you **3 ways** to use the Claude Video Analyzer in your organization:

1. **Command Line (CLI)** - For technical users, batch processing
2. **Web Application (Local)** - Beautiful UI for end users
3. **Docker Deployment** - For enterprise/team deployment

---

## 🎯 Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMPLETE WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SETUP (One-time)                                           │
│     ├─ Install Python & FFmpeg                                 │
│     ├─ Install dependencies                                    │
│     └─ Configure API key                                       │
│                                                                 │
│  2. CHOOSE YOUR METHOD                                         │
│     ├─ CLI: python main.py --video file.mp4                    │
│     ├─ Web UI: python app.py (open browser)                    │
│     └─ Docker: docker-compose up                               │
│                                                                 │
│  3. UPLOAD/SELECT VIDEO                                        │
│     └─ Any format: MP4, AVI, MOV, MKV                          │
│                                                                 │
│  4. CONFIGURE SETTINGS                                         │
│     ├─ Frame interval (2-10 seconds)                           │
│     ├─ Custom prompt (optional)                                │
│     └─ Max frames (cost control)                               │
│                                                                 │
│  5. ANALYZE (Automatic)                                        │
│     ├─ Extract frames from video                               │
│     ├─ Send frames to Claude API                               │
│     └─ Process AI responses                                    │
│                                                                 │
│  6. VIEW RESULTS                                               │
│     ├─ JSON file with analysis                                 │
│     ├─ Extracted frame images                                  │
│     └─ Summary report                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# METHOD 1: Command Line Interface (CLI)

## Best For:
- Technical users comfortable with command line
- Automated/batch processing
- Scripting and integration with other tools

## End-to-End Steps:

### Step 1: One-Time Setup

```bash
# Navigate to project
cd claude-vision-video-analyzer

# Install dependencies (if not done already)
pip install -r requirements.txt

# Configure API key
copy .env.example .env
notepad .env
# Add: ANTHROPIC_API_KEY=your_key_here
```

### Step 2: Basic Usage

```bash
# Analyze a video with defaults
python main.py --video path\to\video.mp4

# That's it! Results saved to output_frames/
```

### Step 3: Advanced Usage

```bash
# Custom frame interval (every 5 seconds = lower cost)
python main.py --video video.mp4 --interval 5

# Custom analysis prompt
python main.py --video video.mp4 \
  --prompt "Identify all people, equipment, and safety issues"

# Save to specific folder
python main.py --video video.mp4 --output my_results

# Limit frames (cost control)
python main.py --video video.mp4 --max-frames 50

# Combine options
python main.py --video video.mp4 \
  --interval 3 \
  --output results_2026 \
  --prompt "Detect defects in product" \
  --verbose
```

### Step 4: View Results

```bash
# Results location
cd output_frames

# View JSON analysis
notepad analysis_20260717_091407.json

# View extracted frames
explorer frames\
```

---

# METHOD 2: Web Application (Local - RECOMMENDED FOR ORG)

## ✨ Best For:
- Non-technical end users
- Drag & drop simplicity
- Beautiful Eli Lilly branded interface
- Real-time progress tracking
- Interactive results viewing

## 🌐 Features:
- ✅ Drag & drop video upload
- ✅ Eli Lilly enterprise design
- ✅ Progress bar with status updates
- ✅ Interactive results display
- ✅ Download JSON results
- ✅ View extracted frames
- ✅ No command line needed!

## End-to-End Steps:

### Step 1: Start the Web Server

```bash
# Navigate to project
cd claude-vision-video-analyzer

# Start Flask web server
python app.py

# You'll see:
# * Running on http://127.0.0.1:5000
# * Running on http://192.168.1.100:5000 (your local IP)
```

### Step 2: Open in Browser

```
Open any browser and go to:
http://localhost:5000

Or share with team using your IP:
http://192.168.1.100:5000
```

### Step 3: Use the Web Interface

1. **Upload Video**
   - Drag & drop video file
   - Or click "Choose File"
   - Supports: MP4, AVI, MOV, MKV, etc.

2. **Configure Settings**
   - Frame Interval: 2-10 seconds (default: 2)
   - Custom Prompt: Optional specific instructions
   - Max Frames: Optional cost limit

3. **Click "Analyze Video"**
   - Watch progress bar
   - See real-time status updates
   - Processing time: ~2-5 seconds per frame

4. **View Results**
   - See analysis on screen
   - Download JSON file
   - View extracted frames
   - Copy/share results

### Step 4: For Organization-Wide Deployment

**Option A: Run on Dedicated Machine**
```bash
# Run server accessible to whole network
python app.py --host 0.0.0.0 --port 5000

# Team members access via:
# http://YOUR_MACHINE_IP:5000
```

**Option B: Use Docker (Recommended for IT)**
```bash
# See "METHOD 3: Docker Deployment" below
docker-compose up -d
```

---

# METHOD 3: Docker Deployment (Enterprise)

## Best For:
- IT department deployments
- Team/organization sharing
- Production environments
- Isolated, secure execution
- Easy updates and maintenance

## Prerequisites:
- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)

## End-to-End Steps:

### Step 1: Create Dockerfile

**NOTE**: Your repo needs a Dockerfile. Let me create one for you.

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for web UI
EXPOSE 5000

# Default command (can be overridden)
CMD ["python", "app.py", "--host", "0.0.0.0"]
```

### Step 2: Configure docker-compose.yml

Update `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: claude-video-analyzer-web
    ports:
      - "5000:5000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - FRAME_INTERVAL=${FRAME_INTERVAL:-2}
    volumes:
      - ./uploads:/app/uploads
      - ./output_frames:/app/output_frames
      - ./.env:/app/.env:ro
    restart: unless-stopped
    command: python app.py --host 0.0.0.0
```

### Step 3: Deploy

```bash
# Build and start
docker-compose up -d

# Access at:
http://localhost:5000

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Step 4: For Production Deployment

```bash
# Add to your .env file
ANTHROPIC_API_KEY=your_key_here
FRAME_INTERVAL=2

# Deploy to server
docker-compose up -d

# Access from any machine in network:
http://SERVER_IP:5000
```

---

# 📊 Complete Workflow Example

## Scenario: Analyzing Security Footage

### Using Web UI (Recommended):

1. **Start Server** (IT Admin - one time)
   ```bash
   python app.py --host 0.0.0.0
   ```

2. **Share URL** with security team
   ```
   http://your-server:5000
   ```

3. **End User Workflow**:
   ```
   ┌─────────────────────────────────────────┐
   │ 1. Open browser → http://server:5000   │
   │ 2. Drag security_cam_footage.mp4       │
   │ 3. Set interval: 5 seconds             │
   │ 4. Prompt: "Identify people, vehicles, │
   │            suspicious activities"       │
   │ 5. Click "Analyze Video"               │
   │ 6. Wait 5-10 minutes (progress shown)  │
   │ 7. View results on screen              │
   │ 8. Download JSON report                │
   │ 9. Share with team                     │
   └─────────────────────────────────────────┘
   ```

4. **Results**:
   - Frame-by-frame analysis
   - People detected: 3 individuals
   - Vehicles: 2 cars, timestamps
   - Suspicious activities: flagged at 00:03:42
   - Full JSON report saved

---

# 🏢 Organization Deployment Guide

## For Your Eli Lilly Team:

### Option 1: Single Shared Server (Simplest)

```bash
# IT Admin sets up once:
1. Install on Windows/Linux server
2. Configure API key in .env
3. Start web server: python app.py --host 0.0.0.0
4. Share URL: http://analysis-server:5000

# End users:
- Open browser
- Go to http://analysis-server:5000
- Upload & analyze videos
- No installation needed!
```

### Option 2: Docker on Server (Recommended)

```bash
# IT Admin:
1. Install Docker on server
2. Clone repository
3. Configure .env with API key
4. Run: docker-compose up -d
5. Share URL: http://analysis-server:5000

# Benefits:
- Isolated environment
- Easy updates (git pull + docker-compose up -d --build)
- Automatic restarts
- Better security
```

### Option 3: Individual Installations

```bash
# Each user installs locally:
1. Clone repository
2. Install Python + FFmpeg
3. Run: pip install -r requirements.txt
4. Configure personal API key (or shared key)
5. Run: python app.py
6. Use at: http://localhost:5000

# Benefits:
- No shared infrastructure needed
- Each user has own instance
- No network dependencies
```

---

# 💰 Cost Management for Organization

## Set Budget Controls:

### In .env file:
```bash
# Limit frame processing
MAX_FRAMES_PER_VIDEO=100

# Minimum interval (reduce API calls)
MIN_FRAME_INTERVAL=5

# Default to budget model
MODEL=claude-3-sonnet-20240229
```

### Usage Monitoring:
```bash
# Track in Anthropic console:
https://console.anthropic.com/settings/usage

# Set spending limits per month
# Monitor usage by API key
# Generate usage reports
```

---

# 🎯 Quick Reference Card

## For End Users (Non-Technical):

```
╔═══════════════════════════════════════════════════════════╗
║         CLAUDE VIDEO ANALYZER - QUICK START              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1. Open browser                                          ║
║  2. Go to: http://analysis-server:5000                    ║
║  3. Drag your video file to upload area                   ║
║  4. Click "Analyze Video"                                 ║
║  5. Wait for results (progress bar shows status)          ║
║  6. Download JSON report when complete                    ║
║                                                           ║
║  ℹ️  Recommended Settings:                                ║
║     Frame Interval: 5 seconds (faster, cheaper)           ║
║     Max Frames: 100 (cost control)                        ║
║                                                           ║
║  💰 Cost: ~$0.50 per minute of video                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## For IT Admins:

```
╔═══════════════════════════════════════════════════════════╗
║         IT DEPLOYMENT - QUICK REFERENCE                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ONE-TIME SETUP:                                          ║
║  ──────────────                                           ║
║  1. git clone <repo>                                      ║
║  2. Configure .env with ANTHROPIC_API_KEY                 ║
║  3. docker-compose up -d                                  ║
║  4. Open firewall port 5000                               ║
║  5. Share URL with team                                   ║
║                                                           ║
║  MAINTENANCE:                                             ║
║  ───────────                                              ║
║  Update:  git pull && docker-compose up -d --build        ║
║  Logs:    docker-compose logs -f                          ║
║  Restart: docker-compose restart                          ║
║  Stop:    docker-compose down                             ║
║                                                           ║
║  MONITORING:                                              ║
║  ──────────                                               ║
║  API usage: https://console.anthropic.com/                ║
║  Server logs: docker-compose logs web                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

# 📞 Support & Troubleshooting

## Common Issues:

### "API key not found"
```bash
# Solution: Check .env file
cat .env
# Should contain: ANTHROPIC_API_KEY=sk-ant-api03-xxx
```

### "FFmpeg not found"
```bash
# Windows: Install via Chocolatey
choco install ffmpeg

# Or download: https://ffmpeg.org/download.html
```

### "Port 5000 already in use"
```bash
# Use different port
python app.py --port 8080

# Access at: http://localhost:8080
```

### Web UI not accessible from other machines
```bash
# Run with --host 0.0.0.0
python app.py --host 0.0.0.0

# Check firewall allows port 5000
```

---

## Next Steps:

1. **Test locally first**: Use CLI with small video
2. **Deploy web UI**: Start Flask server for team access
3. **Set up monitoring**: Track API usage and costs
4. **Train users**: Share Quick Reference Card
5. **Scale as needed**: Move to Docker for production

---

*For detailed technical specs, see COMPLETE_SPECS.md*
