FROM python:3.11-slim

WORKDIR /app

# ------------------------------------------------------------
# Install OS dependencies for OpenCV + video processing
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Install Python dependencies
# ------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------
# Copy source code
# ------------------------------------------------------------
COPY . .

# Cloud Run port
ENV PORT=8080
EXPOSE 8080

# Run FastAPI (server.py)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
