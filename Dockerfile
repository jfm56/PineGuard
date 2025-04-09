# Use multi-stage build for smaller final image
FROM python:3.11-slim-bookworm AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential=12.9 \
    gdal-bin=3.6.4+dfsg-1+b1 \
    libgdal-dev=3.6.4+dfsg-1+b1 \
    git=1:2.39.2-1.1 \
    curl=7.88.1-10+deb12u5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ML model dependencies
RUN pip install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    tensorflow==2.14.0 \
    transformers==4.35.0

# Production image
FROM python:3.11-slim-bookworm

LABEL maintainer="James Mullen <jfm56@github.com>" \
      name="PineGuard" \
      version="1.0.0" \
      description="Advanced Wildfire Risk Prediction System for NJ Pinelands" \
      org.opencontainers.image.source="https://github.com/jfm56/PineGuard" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gdal-bin=3.6.4+dfsg-1+b1 \
    libgdal-dev=3.6.4+dfsg-1+b1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Create necessary directories
RUN mkdir -p /app/data /app/models /app/logs

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV MODEL_DIR=/app/models
ENV LOG_DIR=/app/logs

# Create non-root user
RUN useradd -m -r -s /bin/bash pineguard && \
    chown -R pineguard:pineguard /app

# Switch to non-root user
USER pineguard

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "-m", "app.main"]
