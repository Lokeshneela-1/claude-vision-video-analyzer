# 🏢 Eli Lilly Organization Architecture Alignment

## Overview

This document aligns the Claude Vision Video Analyzer with Eli Lilly's standard architecture and deployment patterns, based on the **nalo-tech-wiki** repository structure.

---

## 📊 Architecture Comparison

### NALO Tech Wiki (Reference Project)
```
Tech Stack:
├─ Node.js (v24-alpine)
├─ Docusaurus (documentation framework)
├─ Docker multi-stage build
├─ GitHub Actions CI/CD
├─ JFrog Artifactory for npm packages
└─ Build → Deploy workflow

Deployment:
├─ Docker containerization
├─ Automated build & push on PR/merge
├─ Environment-based deployments (dev/prod)
└─ Container registry integration
```

### Claude Video Analyzer (Current)
```
Tech Stack:
├─ Python 3.12
├─ Flask (web framework)
├─ FFmpeg (video processing)
├─ Claude Vision API
├─ Docker deployment
└─ Manual deployment

Deployment:
├─ Docker containerization
├─ Manual docker-compose
├─ Local/server deployment
└─ No CI/CD yet
```

---

## 🔄 Alignment Strategy

We'll align the Claude Video Analyzer to follow Eli Lilly's patterns:

### 1. Repository Structure (Aligned)
```
claude-vision-video-analyzer/
├─ .github/
│  ├─ copilot-instructions.md     # (NEW) Copilot agent guidelines
│  ├─ dependabot.yml               # (NEW) Dependency updates
│  └─ workflows/
│     └─ build-and-push.yml        # (NEW) CI/CD pipeline
│
├─ src/                            # (NEW) Source code organization
│  ├─ analyzer.py
│  ├─ app.py
│  ├─ main.py
│  └─ utils.py
│
├─ templates/                      # Flask templates
├─ static/                         # (NEW) Static assets
├─ docs/                           # (NEW) Documentation
├─ tests/                          # (NEW) Test suite
│
├─ Dockerfile                      # ✅ Already present
├─ .dockerignore                   # ✅ Already present
├─ docker-compose.yml              # ✅ Already present
├─ requirements.txt                # ✅ Already present
├─ .gitignore                      # ✅ Already present
├─ README.md                       # ✅ Already present
└─ .env.example                    # ✅ Already present
```

### 2. Docker Multi-Stage Build (Enhanced)

**NALO Pattern:**
- Uses multi-stage build for optimization
- Separates build and runtime dependencies
- Minimizes final image size
- Uses Alpine Linux for small footprint

**Apply to Video Analyzer:**

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install to a venv
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# Set path to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY *.py ./

# Create directories
RUN mkdir -p uploads output_frames

# Non-root user for security
RUN useradd -m -u 1000 analyzer && \
    chown -R analyzer:analyzer /app
USER analyzer

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/status')" || exit 1

# Start application
CMD ["python", "src/app.py", "--host", "0.0.0.0"]
```

### 3. GitHub Actions CI/CD (NEW - Critical)

**Pattern from NALO:**
- Build on PR and push
- Test before merge
- Automatic Docker image building
- Push to container registry
- Environment-based deployments

**Create:** `.github/workflows/build-and-deploy.yml`

```yaml
name: Build and Deploy

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
  push:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  build:
    name: Build Docker Image
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-dev:
    name: Deploy to Development
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: development
      url: https://video-analyzer-dev.lilly.com
    steps:
      - name: Deploy to Dev Environment
        run: |
          echo "Deploying to development environment"
          # Add your deployment script here
          # This could be kubectl, docker-compose, or other deployment tool

  deploy-prod:
    name: Deploy to Production
    needs: build
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://video-analyzer.lilly.com
    steps:
      - name: Deploy to Production
        run: |
          echo "Deploying to production environment"
          # Add your production deployment script here
```

### 4. Copilot Instructions (NEW)

**Pattern from NALO:**
- Repository-specific guidelines for Copilot
- Code standards and conventions
- Common patterns and best practices

**Create:** `.github/copilot-instructions.md`

```markdown
# GitHub Copilot Instructions for Claude Vision Video Analyzer

## Project Overview
This is a Python-based video analysis tool using Claude's Vision API to analyze video frames.

## Code Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for all classes and functions

### File Organization
- Core logic in `src/` directory
- Web UI code in `app.py`
- CLI interface in `main.py`
- Utilities in `utils.py`

### Naming Conventions
- Classes: PascalCase (e.g., `VideoAnalyzer`)
- Functions: snake_case (e.g., `analyze_frame`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_FRAMES`)
- Private methods: _snake_case (e.g., `_extract_frames`)

### Error Handling
- Use try/except for API calls
- Log errors with appropriate severity
- Return meaningful error messages to users
- Never expose API keys in error messages

### Security
- Never commit API keys
- Use environment variables for secrets
- Validate all user inputs
- Sanitize file uploads
- Use secure headers in Flask

### Testing
- Write unit tests for all core functions
- Use pytest framework
- Mock API calls in tests
- Aim for 80%+ code coverage

## Common Patterns

### API Call Pattern
```python
try:
    response = client.messages.create(
        model=self.model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text
except Exception as e:
    logger.error(f"API call failed: {e}")
    raise
```

### File Upload Pattern
```python
filename = secure_filename(file.filename)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
saved_filename = timestamp + filename
filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
file.save(filepath)
```

### Environment Variable Pattern
```python
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")
```

## Dependencies
- Keep `requirements.txt` minimal
- Pin major versions for stability
- Document why each dependency is needed
- Regular security updates via Dependabot

## Docker
- Use multi-stage builds for optimization
- Run as non-root user
- Include health checks
- Use .dockerignore to exclude unnecessary files

## Documentation
- Update README.md for major changes
- Keep WORKFLOW_GUIDE.md current
- Add examples for new features
- Document all API endpoints
```

### 5. Dependabot Configuration (NEW)

**Create:** `.github/dependabot.yml`

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"
    reviewers:
      - "Lokeshneela-1"

  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 3
    labels:
      - "dependencies"
      - "docker"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    labels:
      - "dependencies"
      - "github-actions"
```

### 6. Enhanced .dockerignore

**Pattern from NALO** - Exclude unnecessary files:

```
# Git files
.git
.gitignore
.gitattributes

# Python specific
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Documentation (not needed in container)
docs/
*.md
!README.md

# CI/CD
.github/

# Local development
.env
.env.local
uploads/
output_frames/
videos/

# Windows
Thumbs.db
ehthumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
```

---

## 🚀 Implementation Plan

### Phase 1: Immediate (This Week)
- [ ] Create `.github/` directory structure
- [ ] Add Copilot instructions
- [ ] Add Dependabot configuration
- [ ] Update .dockerignore
- [ ] Reorganize code into `src/` directory

### Phase 2: CI/CD Setup (Next Week)
- [ ] Create GitHub Actions workflow
- [ ] Set up automated testing
- [ ] Configure Docker image build & push
- [ ] Set up GitHub Container Registry

### Phase 3: Testing & Quality (Week 3)
- [ ] Add pytest test suite
- [ ] Add code coverage reporting
- [ ] Add linting (flake8, black)
- [ ] Add security scanning

### Phase 4: Deployment Automation (Week 4)
- [ ] Set up development environment
- [ ] Set up production environment
- [ ] Configure automated deployments
- [ ] Add monitoring and logging

---

## 📝 Key Differences to Address

### 1. Package Management
**NALO:** npm with JFrog Artifactory  
**Video Analyzer:** pip with PyPI

**Solution:**  
- Use pip-tools for reproducible builds
- Consider internal PyPI mirror if needed
- Pin all dependencies with exact versions

### 2. Build Process
**NALO:** npm build → static site  
**Video Analyzer:** Python app → runtime server

**Solution:**  
- Use multi-stage Docker build
- Compile Python bytecode in build stage
- Minimize runtime dependencies

### 3. Deployment Target
**NALO:** Static documentation site  
**Video Analyzer:** Dynamic web application

**Solution:**  
- Add load balancing considerations
- Implement proper session management
- Add rate limiting for API calls
- Configure proper health checks

---

## 🔒 Security Enhancements

Following Eli Lilly security standards:

### 1. Container Security
```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 analyzer && \
    chown -R analyzer:analyzer /app
USER analyzer

# Read-only root filesystem (where possible)
# Drop unnecessary capabilities
# Use security scanning tools
```

### 2. API Key Management
```yaml
# Use GitHub Secrets
secrets:
  ANTHROPIC_API_KEY:
    required: true

# Or Azure Key Vault integration
# Or AWS Secrets Manager
```

### 3. Network Security
```yaml
# Implement network policies
# Use TLS/SSL for all communications
# Restrict container capabilities
# Enable AppArmor/SELinux
```

---

## 📊 Monitoring & Observability

Add instrumentation similar to Eli Lilly standards:

### 1. Application Metrics
```python
from prometheus_client import Counter, Histogram

video_analysis_count = Counter('video_analyses_total', 'Total video analyses')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis duration')

@analysis_duration.time()
def analyze_video(video_path):
    video_analysis_count.inc()
    # ... analysis code
```

### 2. Health Checks
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'dependencies': {
            'ffmpeg': check_ffmpeg(),
            'api': check_anthropic_api(),
            'disk_space': check_disk_space()
        }
    })
```

### 3. Logging
```python
import logging
import structlog

# Structured logging for better observability
logger = structlog.get_logger()

logger.info(
    "video_analysis_started",
    video_path=video_path,
    frame_interval=interval,
    user_id=user_id
)
```

---

## 🎯 Next Steps

1. **Review this alignment document** with your team
2. **Prioritize** which enhancements to implement first
3. **Create issues** in GitHub for each enhancement
4. **Set up CI/CD pipeline** as top priority
5. **Add tests** before automating deployments
6. **Document** deployment procedures for Lilly IT

---

## 📞 Support & Questions

For Eli Lilly specific requirements:
- Check dev.lilly.com for platform standards
- Consult with NALO Tech team for best practices
- Review other Eli Lilly GitHub repos for patterns

---

*This alignment ensures the Claude Video Analyzer follows Eli Lilly's established patterns for maintainability, security, and scalability.*
