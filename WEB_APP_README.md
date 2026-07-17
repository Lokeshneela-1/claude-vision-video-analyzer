# 🌐 Web Application Deployment Guide

## Quick Start for End Users

### Windows (Double-Click to Start!)

1. **Download the repository**
2. **Double-click**: `start_webapp.bat`
3. **Open browser**: http://localhost:5000
4. **Upload and analyze videos!**

That's it! The script handles everything automatically.

---

## Manual Setup

### Prerequisites
- Python 3.9+ installed
- FFmpeg installed
- Claude API key from https://console.anthropic.com/

### Step 1: Install Dependencies

```bash
# Navigate to project folder
cd claude-vision-video-analyzer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Copy template
copy .env.example .env

# Edit .env and add your API key
notepad .env

# Add this line:
ANTHROPIC_API_KEY=sk-ant-api03-xxxYOURKEYxxx
```

### Step 3: Create templates folder

```bash
# Create folder
mkdir templates

# Copy index.html
copy index.html templates\index.html
```

### Step 4: Start Web Server

```bash
# Option 1: Local access only (default)
python app.py

# Option 2: Network access (share with team)
python app.py --host 0.0.0.0

# Option 3: Custom port
python app.py --port 8080

# Option 4: Debug mode
python app.py --debug
```

### Step 5: Access the Application

Open your browser and go to:
- **Local**: http://localhost:5000
- **Network** (if using --host 0.0.0.0): http://YOUR_IP:5000

---

## Features

### ✨ User Interface
- **Drag & Drop Upload**: Simply drag video files to upload
- **Eli Lilly Branding**: Professional enterprise design
- **Progress Tracking**: Real-time progress bar during analysis
- **Interactive Results**: View analysis on screen
- **Download Reports**: Get JSON results

### 🎛️ Configuration Options
- **Frame Interval**: 1-10 seconds (default: 2)
- **Custom Prompts**: Tailor analysis to your needs
- **Max Frames**: Limit processing for cost control
- **Model Selection**: Choose Claude model (configurable)

### 📊 Results
- Frame-by-frame analysis
- Objects detected
- Actions identified
- Text extraction
- Overall context
- Downloadable JSON report

---

## Organization Deployment

### For IT Administrators

#### Option 1: Dedicated Server (Recommended)

1. **Setup server** (Windows/Linux)
2. **Install dependencies** (Python, FFmpeg)
3. **Clone repository**
4. **Configure API key** in .env
5. **Start server**:
   ```bash
   python app.py --host 0.0.0.0 --port 5000
   ```
6. **Configure firewall** to allow port 5000
7. **Share URL with team**: http://server-name:5000

#### Option 2: Docker Deployment (Enterprise)

1. **Install Docker** on server
2. **Clone repository**
3. **Configure .env** with API key
4. **Start container**:
   ```bash
   docker-compose up -d
   ```
5. **Access at**: http://server-ip:5000

```yaml
# docker-compose.yml is already configured
# Just run: docker-compose up -d
```

#### Option 3: Cloud Deployment (Azure/AWS)

1. **Create VM** (Windows Server or Linux)
2. **Install dependencies**
3. **Clone repository**
4. **Configure** .env with API key
5. **Start as service** (systemd on Linux, Task Scheduler on Windows)
6. **Configure security group** to allow port 5000
7. **Optional**: Setup reverse proxy (nginx) with SSL

---

## Security Considerations

### For Production Deployment

1. **API Key Protection**
   - Never commit .env to Git
   - Use environment variables
   - Rotate keys regularly
   - Separate keys for dev/production

2. **Network Security**
   - Use HTTPS (SSL/TLS)
   - Setup reverse proxy (nginx/Apache)
   - Implement authentication if needed
   - Restrict to corporate network only

3. **File Upload Security**
   - Already limited to video formats
   - 500MB max file size configured
   - Files stored in isolated uploads folder
   - Implement virus scanning if needed

4. **Cost Controls**
   - Set API spending limits in Anthropic console
   - Monitor usage regularly
   - Implement per-user quotas if needed
   - Use MAX_FRAMES environment variable

---

## Usage Examples

### Example 1: Security Footage Analysis

```
1. Open: http://localhost:5000
2. Upload: security_cam_2026-07-17.mp4
3. Settings:
   - Frame Interval: 5 seconds
   - Custom Prompt: "Identify people, vehicles, and any unusual activities"
4. Analyze
5. Results: Detailed timeline of events
```

### Example 2: Product Quality Inspection

```
1. Open: http://localhost:5000
2. Upload: production_line_recording.mp4
3. Settings:
   - Frame Interval: 2 seconds
   - Custom Prompt: "Inspect products for defects, damaged packaging, or quality issues"
4. Analyze
5. Results: Frame-by-frame quality report
```

### Example 3: Training Video Analysis

```
1. Open: http://localhost:5000
2. Upload: safety_training_video.mp4
3. Settings:
   - Frame Interval: 10 seconds
   - Custom Prompt: "Identify key training points, safety equipment, and procedures shown"
4. Analyze
5. Results: Training content summary
```

---

## Monitoring & Maintenance

### Check Server Status

```bash
# Server should show:
# * Running on http://0.0.0.0:5000
# * Press CTRL+C to stop
```

### View Logs

```bash
# Application logs are printed to console
# Redirect to file:
python app.py > server.log 2>&1

# Or use Docker:
docker-compose logs -f
```

### Monitor API Usage

1. Go to: https://console.anthropic.com/settings/usage
2. View usage by API key
3. Set spending alerts
4. Generate monthly reports

### Update Application

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart server
# (Stop with Ctrl+C, then start again)
python app.py --host 0.0.0.0
```

---

## Troubleshooting

### Problem: "Template not found"

**Solution**:
```bash
mkdir templates
copy index.html templates\index.html
```

### Problem: "Port 5000 already in use"

**Solution**:
```bash
# Use different port
python app.py --port 8080
```

### Problem: "API key not configured"

**Solution**:
```bash
# Check .env file exists
dir .env

# Check contents
type .env

# Should contain:
# ANTHROPIC_API_KEY=sk-ant-api03-xxx...
```

### Problem: "FFmpeg not found"

**Solution**:
```bash
# Windows - Install via Chocolatey:
choco install ffmpeg

# Or download from:
https://ffmpeg.org/download.html
```

### Problem: Can't access from other machines

**Solution**:
```bash
# 1. Start with network access
python app.py --host 0.0.0.0

# 2. Check firewall allows port 5000
# Windows Firewall: Add inbound rule for port 5000

# 3. Find your IP address
ipconfig

# 4. Share URL: http://YOUR_IP:5000
```

---

## Performance Tips

### For Better Performance

1. **Frame Interval**: Use 5-10 seconds for faster processing
2. **Max Frames**: Limit to 100-200 frames for large videos
3. **Server Resources**: Minimum 4GB RAM recommended
4. **Network**: Good internet connection for API calls
5. **Concurrent Users**: ~5-10 users per server (adjust resources)

### Cost Optimization

1. **Default interval**: Set to 5 seconds in .env
2. **Model selection**: Use Claude 3 Sonnet (faster, cheaper)
3. **Max frames**: Set limit to prevent expensive jobs
4. **User training**: Educate on cost-effective settings

---

## System Requirements

### Server Requirements
- **OS**: Windows Server 2016+, Ubuntu 20.04+, or similar
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 50GB+ (for uploaded videos and frames)
- **Network**: Stable internet for API calls

### Client Requirements (End Users)
- **Browser**: Chrome, Firefox, Edge, Safari (recent versions)
- **Network**: Access to server (LAN or VPN)
- **No installation needed!** Just browser access

---

## Support

### For End Users
- Open browser → http://server:5000
- Drag video file
- Click "Analyze"
- Download results

### For IT Support
- Check server is running
- Verify API key in .env
- Check firewall rules
- Monitor logs for errors
- Review API usage in Anthropic console

### Documentation
- **Workflow Guide**: WORKFLOW_GUIDE.md
- **Complete Specs**: COMPLETE_SPECS.md
- **Main README**: README.md

---

## Quick Reference

### Start Server (Windows)
```bash
# Easy way
start_webapp.bat

# Manual way
python app.py --host 0.0.0.0
```

### Start Server (Linux/Production)
```bash
# Development
python app.py --host 0.0.0.0

# Production (with Docker)
docker-compose up -d

# Production (with systemd)
sudo systemctl start claude-analyzer
```

### Access URLs
- Local: http://localhost:5000
- Network: http://SERVER_IP:5000
- Production: https://analyzer.yourcompany.com

---

*Eli Lilly Enterprise Edition | Powered by Claude AI*
