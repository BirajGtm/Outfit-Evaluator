# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git, build-essential for some packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Create uploads directory with proper permissions
RUN mkdir -p /data/uploads && chmod 777 /data/uploads

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Explicitly verify the model file is copied and show directory structure
RUN echo "=== Checking if model file was copied ===" && \
    ls -la app/ || echo "app/ directory not found" && \
    ls -la app/best.pt || echo "best.pt not found in app/" && \
    echo "=== Directory structure check complete ==="

# Set environment variables for Cloud Run
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start the app
CMD ["python", "run.py"]
