# Local Whisper Transcription

This project allows you to transcribe videos using a local Whisper model running in a container.

## Prerequisites

- [Podman](https://podman.io/) (or Docker)

## Build

Build the container image:

```powershell
podman build -t whisper-local .
```

## Run

Run the transcription on a video file located in the current directory:

```powershell
podman run --rm -v ${PWD}:/app whisper-local <your_video_filename>
```

### Example

```powershell
podman run --rm -v ${PWD}:/app whisper-local my_meeting.mp4
```
