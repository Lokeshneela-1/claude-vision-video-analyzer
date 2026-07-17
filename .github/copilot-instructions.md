# GitHub Copilot Instructions for Claude Vision Video Analyzer

## Project Overview
This is an enterprise-grade Python application for analyzing video content using Claude's Vision API. Built for Eli Lilly's NALO organization.

## 🏢 Eli Lilly Standards

This project follows Eli Lilly's development standards as established in the nalo-tech-wiki and other NALO projects.

### Code Quality
- Follow PEP 8 Python style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Docstrings required for all public classes and functions
- Run Black formatter before commits
- Use isort for import organization

### Security First
- **NEVER** commit API keys, tokens, or secrets
- Use environment variables for all sensitive data
- Validate and sanitize all user inputs
- Use secure_filename() for all file uploads
- Run as non-root user in containers
- Regular dependency updates via Dependabot

## 📁 File Organization

```
claude-vision-video-analyzer/
├─ src/                    # Source code
│  ├─ analyzer.py          # Core video analysis engine
│  ├─ app.py               # Flask web application
│  ├─ main.py              # CLI interface
│  └─ utils.py             # Utility functions
├─ templates/              # Flask templates
├─ static/                 # Static assets (CSS, JS, images)
├─ tests/                  # Test suite
├─ docs/                   # Documentation
└─ .github/                # GitHub Actions & configs
```

## 🎯 Naming Conventions

### Python
- **Classes**: PascalCase (e.g., `VideoAnalyzer`, `FrameExtractor`)
- **Functions**: snake_case (e.g., `analyze_frame`, `extract_frames`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_FRAMES`, `DEFAULT_INTERVAL`)
- **Private methods**: _snake_case (e.g., `_validate_input`, `_clean_temp_files`)
- **Environment variables**: UPPER_SNAKE_CASE (e.g., `ANTHROPIC_API_KEY`)

### Files
- **Python modules**: snake_case.py
- **Test files**: test_*.py
- **Documentation**: UPPER_CASE.md (e.g., README.md, SETUP_GUIDE.md)

## 🔒 Security Patterns

### Environment Variables
```python
# Always check for required environment variables
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")
```

### File Upload Security
```python
from werkzeug.utils import secure_filename
from datetime import datetime

# Always sanitize file names and add timestamps
filename = secure_filename(file.filename)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
safe_filename = timestamp + filename
filepath = os.path.join(UPLOAD_DIR, safe_filename)
```

### API Call Pattern with Error Handling
```python
try:
    response = client.messages.create(
        model=self.model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text
except anthropic.APIError as e:
    logger.error(f"Claude API error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error during API call: {e}")
    raise
```

## 🧪 Testing Standards

### Test Structure
```python
import pytest
from unittest.mock import Mock, patch

class TestVideoAnalyzer:
    def test_initialization(self):
        """Test VideoAnalyzer initialization"""
        analyzer = VideoAnalyzer(output_dir="test_output")
        assert analyzer.output_dir == Path("test_output")
    
    @patch('analyzer.Anthropic')
    def test_analyze_frame_success(self, mock_anthropic):
        """Test successful frame analysis"""
        # Setup mock
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        
        # Test code
        analyzer = VideoAnalyzer()
        result = analyzer.analyze_frame("frame.jpg")
        
        # Assertions
        assert result is not None
        mock_client.messages.create.assert_called_once()
```

### Coverage Goals
- Aim for 80%+ code coverage
- All core functions must have tests
- Mock external API calls
- Test error conditions
- Test edge cases

## 📦 Dependency Management

### Adding Dependencies
```bash
# Add to requirements.txt with version pinning
anthropic==0.18.1  # Claude API
flask==3.0.0       # Web framework
```

### Dependency Rules
- Pin all dependencies to specific versions
- Document why each dependency is needed
- Regular security updates via Dependabot
- Keep dependencies minimal
- Prefer standard library when possible

## 🐳 Docker Best Practices

### Multi-Stage Builds
Always use multi-stage builds to reduce image size:
```dockerfile
# Builder stage
FROM python:3.12-slim as builder
# ... build steps

# Runtime stage
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
```

### Security
- Run as non-root user
- Use minimal base images (slim/alpine)
- Include health checks
- Scan for vulnerabilities
- Keep base images updated

### Example Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/status')" || exit 1
```

## 🚀 Flask Application Standards

### Route Structure
```python
@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyze uploaded video"""
    try:
        # 1. Validate request
        if 'video' not in request.files:
            return jsonify({'error': 'No video file'}), 400
        
        # 2. Process
        result = process_video(request.files['video'])
        
        # 3. Return structured response
        return jsonify({
            'status': 'success',
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_video: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
```

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500
```

## 📝 Logging Standards

### Structured Logging
```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Frame extraction started")
logger.info(f"Analyzing video: {video_path}")
logger.warning(f"Frame interval {interval} is unusually high")
logger.error(f"API call failed: {error}")
logger.critical(f"System out of disk space")
```

### Log Format
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔄 Git Commit Standards

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes

### Examples
```
feat(analyzer): add support for custom frame intervals

Added ability to specify custom frame extraction intervals
to reduce API costs and processing time.

Closes #42
```

```
fix(api): handle missing API key gracefully

Previously crashed with unclear error. Now returns
user-friendly message and logs the issue.
```

## 📚 Documentation Standards

### Code Documentation
```python
def analyze_frame(
    self,
    frame_path: str,
    custom_prompt: Optional[str] = None,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    Analyze a single video frame using Claude Vision API.
    
    Args:
        frame_path: Path to the frame image file
        custom_prompt: Optional custom analysis prompt
        max_tokens: Maximum tokens in API response
        
    Returns:
        Dict containing analysis results with keys:
            - objects: List of detected objects
            - actions: Description of actions
            - text: Any visible text
            - context: Overall context
            
    Raises:
        FileNotFoundError: If frame_path doesn't exist
        anthropic.APIError: If Claude API call fails
        
    Example:
        >>> analyzer = VideoAnalyzer()
        >>> result = analyzer.analyze_frame("frame_001.jpg")
        >>> print(result['objects'])
        ['person', 'desk', 'computer']
    """
    # Implementation
```

### README Updates
When adding features, update:
- Feature list
- Usage examples
- API documentation
- Troubleshooting section

## ⚡ Performance Considerations

### Async Processing
For I/O-bound operations, consider async:
```python
import asyncio
import aiohttp

async def analyze_frames_async(frames: List[str]):
    tasks = [analyze_frame_async(frame) for frame in frames]
    results = await asyncio.gather(*tasks)
    return results
```

### Resource Management
```python
# Always use context managers
with open(frame_path, 'rb') as f:
    data = f.read()

# Clean up temporary files
try:
    # Process frames
    pass
finally:
    for frame in temp_frames:
        os.remove(frame)
```

## 🎨 UI/UX Standards

### Eli Lilly Branding
- Primary Blue: #003DA5
- Light Blue: #0057B8
- Professional, clean design
- Responsive layouts
- Accessibility (WCAG 2.1 AA)

### User Feedback
- Show progress for long operations
- Clear error messages
- Success confirmations
- Loading states

## 🔍 Code Review Checklist

Before submitting PR:
- [ ] All tests pass
- [ ] Code coverage ≥ 80%
- [ ] No secrets in code
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Black & isort run
- [ ] Security scan clean
- [ ] Docker build succeeds

## 🆘 Common Issues

### Import Errors
Always use absolute imports:
```python
# Good
from src.analyzer import VideoAnalyzer
from src.utils import print_info

# Bad
from analyzer import VideoAnalyzer
```

### Path Issues
Use pathlib for cross-platform compatibility:
```python
from pathlib import Path

output_dir = Path("output") / "frames"
output_dir.mkdir(parents=True, exist_ok=True)
```

## 📞 Getting Help

- Check existing documentation in `docs/`
- Review similar code in the repository
- Consult Eli Lilly dev portal: dev.lilly.com
- Ask NALO Tech team for guidance

---

**Remember**: Security, quality, and maintainability are priorities. When in doubt, ask for review!
