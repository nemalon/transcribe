# Local Whisper Transcription

This project allows you to transcribe video and audio files using a local Whisper model running efficiently inside a Docker container.

## 🚀 Key Features

* **GPU Acceleration:** Utilize your NVIDIA GPU (including older architectures like GTX 1080) for significantly faster transcription.
* **Persistent Caching:** Save the large Whisper model files in a Docker volume to avoid re-downloading them on every run.
* **Containerized Environment:** Ensures a consistent, isolated environment without polluting your host system dependencies.

## 🛠️ Build Requirements

The Docker build process ensures PyTorch compatibility with your specific GPU architecture (sm_61). Your Dockerfile uses a dynamic build argument to install the correct CUDA-compatible PyTorch binaries.

| GPU Architecture | CUDA Index URL (for `--build-arg`) | Example GPU |
| :--- | :--- | :--- |
| **sm_61** (Pascal) | `https://download.pytorch.org/whl/cu126` (Default) | **GTX 1080** |
| sm_75 (Turing) | *(May use standard PyPI index)* | RTX 2070 |

### Build Command

Build the container image using the default settings for GTX 1080 compatibility:

```bash
sudo docker build -t whisper-local:sm61 .
```

## 🏃 Run Requirements

* **Docker Desktop:** Installed and running (using the WSL 2 backend if on Windows).
* **NVIDIA Container Toolkit:** Installed and configured on your host system to allow Docker to access your NVIDIA GPU (required for the `--gpus all` flag).

### Step 1: Create the Cache Volume

Create a persistent volume so that Whisper models are downloaded only once.

```bash
docker volume create whisper-cache-volume
```

### Step 2: Run Transcription

Run the transcription on a video file located in your current directory.

**Syntax:**

```bash
sudo docker run --rm --gpus all \
    -v $(pwd):/app \
    -v whisper-cache-volume:/root/.cache/whisper \
    whisper-local:sm61 \
    <filename> [model_size]
```

**Parameters:**

* `--rm`: Automatically remove the container when finished.
* `--gpus all`: Pass the host GPU to the container.
* `-v $(pwd):/app`: Mount the current directory to the container so the script can find your video.
* `-v whisper-cache-volume:/root/.cache/whisper`: Mount the cache volume to save models.

---

## 📝 Examples

### Example 1: Basic Run (Default Model)
Transcribe `meeting_recording.mp4` using the default `base` model.

```bash
sudo docker run --rm --gpus all \
    -v $(pwd):/app \
    -v whisper-cache-volume:/root/.cache/whisper \
    whisper-local:sm61 \
    meeting_recording.mp4
```

### Example 2: High Accuracy (Medium Model)
Transcribe `lecture.mp4` using the `medium` model for better accuracy.

```bash
sudo docker run --rm --gpus all \
    -v $(pwd):/app \
    -v whisper-cache-volume:/root/.cache/whisper \
    whisper-local:sm61 \
    lecture.mp4 medium
```

# Expected output
```
docker run --rm --gpus all     -v $(pwd):/app     -v whisper-cache-volume:/root/.cache/whisper     whisper-local:sm61 'foi.mp4'
--- Initialization ---
Device: CUDA
Media Duration: 4934.54 seconds
Loading 'base' model...
--- Starting Transcription ---
 73%|███████▎  | 3581.7/4934.541667s [41:18<15:36]

--- Saving Files ---
Saved: foi.txt
Saved: foi.srt
--- Done ---
```