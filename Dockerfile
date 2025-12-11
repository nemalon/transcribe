FROM python:3.10-slim

# Install system dependencies (ffmpeg is required for whisper audio processing)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir openai-whisper torch

WORKDIR /app

# Run the script
ENTRYPOINT ["python", "main.py"]
