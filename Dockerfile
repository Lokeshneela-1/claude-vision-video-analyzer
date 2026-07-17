# ================================
# Stage 1: Builder
# ================================
FROM python:3.14-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install to a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ================================
# Stage 2: Runtime
# ================================
FROM python:3.14-slim

# Build arguments for metadata
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.0.0

# Metadata labels
LABEL org.opencontainers.image.title="Claude Vision Video Analyzer"
LABEL org.opencontainers.image.description="Enterprise video analysis using Claude Vision API"
LABEL org.opencontainers.image.authors="Lokesh Neela <lokesh.neela@network.lilly.com>"
LABEL org.opencontainers.image.vendor="Eli Lilly and Company - NALO"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.version="${VERSION}"

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set path to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY analyzer.py app.py main.py utils.py ./
COPY templates/ ./templates/

# Create necessary directories
RUN mkdir -p uploads output_frames static

# Create non-root user for security (following Eli Lilly standards)
RUN useradd -m -u 1000 -s /bin/bash analyzer && \
    chown -R analyzer:analyzer /app && \
    chmod -R 755 /app

# Switch to non-root user
USER analyzer

# Expose port for web UI
EXPOSE 5000

# Environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    NODE_OPTIONS='--max-http-header-size=65536'

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/status')" || exit 1

# Start application
CMD ["python", "app.py", "--host", "0.0.0.0"]
