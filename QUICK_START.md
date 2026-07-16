# Project Summary & Quick Start

## 📦 What's Included

This complete project replaces the Ollama-based video analyzer with Claude's Vision API. 

**Files & Directories:**

```
claude-vision-video-analyzer/
├── main.py                 # CLI entry point
├── analyzer.py             # Core video analysis engine
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── .gitignore             # Git ignore patterns
├── LICENSE                # MIT License
│
├── README.md              # Main documentation
├── SETUP_GUIDE.md         # Setup instructions
├── END_TO_END_GUIDE.md    # Complete implementation guide
│
├── test_setup.py          # Setup verification script
│
└── examples/              # Example scripts
    ├── 01_basic_analysis.py
    ├── 02_custom_prompts.py
    └── 03_batch_processing.py
```

## ⚡ Quick Start (5 Minutes)

### 1. Prerequisites
```bash
# Verify you have Python 3.9+, FFmpeg, and API key
python --version
ffmpeg -version
# API key from: https://console.anthropic.com/
```

### 2. Setup
```bash
# Clone/download project
cd claude-vision-video-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your API key
```

### 3. Test
```bash
python test_setup.py
```

### 4. First Analysis
```bash
python main.py --video your_video.mp4
```

## 🚀 Main Features

✅ **Extract Frames** - From any video format (MP4, AVI, MOV, etc.)
✅ **Claude Vision** - Professional AI analysis of each frame
✅ **Structured Output** - JSON results with detailed analysis
✅ **Batch Processing** - Handle multiple videos
✅ **Custom Prompts** - Tailor analysis for your use case
✅ **Progress Tracking** - Visual feedback during processing
✅ **Error Handling** - Robust error recovery

## 📚 Documentation

1. **[README.md](README.md)** - Overview & features
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation & basic usage
3. **[END_TO_END_GUIDE.md](END_TO_END_GUIDE.md)** - Complete implementation guide with every detail
4. **[Examples](examples/)** - Real-world usage examples

## 💡 Common Use Cases

```bash
# Sports analysis
python main.py --video game.mp4 --interval 0.5 \
  --prompt "Identify plays, athletes, and moments"

# Security monitoring
python main.py --video security.mp4 \
  --prompt "Report suspicious activities"

# Educational content
python main.py --video lecture.mp4 \
  --prompt "Extract key concepts and formulas"

# Content cataloging
python main.py --video content.mp4 --interval 10 \
  --output catalog_results
```

## 📊 API Costs

Typical costs per video:

| Duration | Interval | Frames | Cost* |
|----------|----------|--------|-------|
| 1 min    | 2s       | 30     | $0.07 |
| 5 min    | 2s       | 150    | $0.36 |
| 10 min   | 5s       | 120    | $0.29 |
| 1 hour   | 10s      | 360    | $0.86 |

*Based on Claude 3.5 Sonnet (~$0.003 per image)

## 🆚 vs Original (Ollama-based)

| Aspect | Ollama | Claude API |
|--------|--------|-----------|
| **Setup** | Complex | Simple |
| **Hardware** | Required | None |
| **Speed** | Slow | Fast |
| **Quality** | Good | Excellent |
| **Cost** | Free* | $0.003/image |
| **Maintenance** | Manual | Managed |
| **Scalability** | Limited | Unlimited |

## 🔑 API Keys & Security

⚠️ **Important Security Notes:**

1. **Get your API key:**
   - Go to https://console.anthropic.com/
   - Create account (free)
   - Generate API key from "API Keys" section

2. **Protect your key:**
   - Never commit `.env` to git
   - Never share your key
   - Use environment variables in production
   - Rotate keys regularly

3. **Cost control:**
   - Monitor usage in Anthropic dashboard
   - Set spending limits
   - Test with small videos first

## 🧪 Testing

```bash
# Run setup verification
python test_setup.py

# Analyze a test video
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=5 \
        -f lavfi -i sine=f=1000:d=5 \
        -pix_fmt yuv420p test_video.mp4

python main.py --video test_video.mp4
```

## 📁 Output

Results are saved in `output_frames/{video_name}/`:

- **frames/** - Extracted frame images
- **analysis_results.json** - Detailed analysis in JSON
- **summary.txt** - Human-readable summary

## 🆘 Troubleshooting

**FFmpeg not found:**
```bash
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
choco install ffmpeg  # Windows
```

**API key not found:**
```bash
# Create .env file with your key
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

**Video not processing:**
```bash
# Verify video works
ffprobe your_video.mp4
# Try different format or convert first
```

## 🎯 Next Steps

1. Follow **[END_TO_END_GUIDE.md](END_TO_END_GUIDE.md)** for detailed setup
2. Run **test_setup.py** to verify installation
3. Try examples in **examples/** directory
4. Integrate into your application

## 📝 Examples

Check `examples/` directory:

1. **01_basic_analysis.py** - Simple video analysis
2. **02_custom_prompts.py** - Different analysis types
3. **03_batch_processing.py** - Multiple videos & searching

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## 💬 Support

- **Issues:** GitHub issues with error details
- **Questions:** See FAQ in END_TO_END_GUIDE.md
- **Documentation:** Read SETUP_GUIDE.md & END_TO_END_GUIDE.md

---

## Ready to Go?

```bash
# Quick start
cd claude-vision-video-analyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python test_setup.py
python main.py --video your_video.mp4
```

**Questions? Read [END_TO_END_GUIDE.md](END_TO_END_GUIDE.md) for comprehensive documentation.**

**Happy analyzing! 🎉**
