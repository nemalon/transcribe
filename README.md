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
| **sm\_61** (Pascal) | `https://download.pytorch.org/whl/cu126` (Default) | **GTX 1080** |
| sm\_75 (Turing) | *(May use standard PyPI index)* | RTX 2070 |

Build the container image:

```bash
# Build command for GTX 1080 (sm_61): Uses the default cu126 index set in the Dockerfile
sudo docker build -t whisper-local:sm61 .