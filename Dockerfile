FROM python:3.10-slim

# Define a build argument for the PyTorch index URL.
# Default is set to CUDA 12.6, which is compatible with GTX 1080 (sm_61).
ARG PYTORCH_INDEX_URL="https://download.pytorch.org/whl/cu126"

# Install system dependencies (ffmpeg is required for whisper audio processing)
# Ensure the root file system is clean afterward
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies. 
# Use --extra-index-url so pip can find openai-whisper on PyPI and the custom 
# torch version on the PyTorch index.
RUN pip install --no-cache-dir \
    openai-whisper \
    torch torchvision torchaudio \
    --extra-index-url ${PYTORCH_INDEX_URL}

WORKDIR /app

# The ENTRYPOINT runs the main.py script with the provided filename as an argument.
ENTRYPOINT ["python", "main.py"]