# Production Dockerfile for Google Cloud Run Deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Generate sample inspection benchmark assets
RUN python generate_sample_images.py

# Expose Cloud Run default container port
EXPOSE 8080

# Healthcheck configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Launch Streamlit server bound to 0.0.0.0:$PORT
ENTRYPOINT ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false --server.headless=true"]
