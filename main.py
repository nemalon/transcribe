import sys
import os
import re
import subprocess
import whisper
import torch
from tqdm import tqdm

# Regex to extract the "end" timestamp from Whisper logs
# Format: [00:12.000 --> 00:14.500]
TIMESTAMP_PATTERN = re.compile(r"\[.*--> (\d{2}:\d{2}\.\d{3})\]")

def get_duration(filename):
    """
    Get the duration of the media file in seconds using ffprobe.
    """
    try:
        command = [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            filename
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception:
        return None

def parse_timestamp_to_seconds(timestamp_str):
    """Converts '00:14.500' (MM:SS.mmm) to seconds."""
    try:
        minutes, seconds = timestamp_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except ValueError:
        return 0.0

class ProgressOutput:
    """
    Captures stdout, parses Whisper timestamps, and updates a tqdm progress bar.
    """
    def __init__(self, total_duration):
        self.pbar = tqdm(total=total_duration, unit="s", bar_format="{l_bar}{bar}| {n:.1f}/{total_fmt}s [{elapsed}<{remaining}]")
        self.terminal = sys.stdout # Keep a handle to the real terminal

    def write(self, message):
        # Check if the message contains a Whisper timestamp
        match = TIMESTAMP_PATTERN.search(message)
        if match:
            current_time_str = match.group(1)
            current_seconds = parse_timestamp_to_seconds(current_time_str)
            
            # Update the progress bar to the current timestamp
            # We use 'n' to set absolute position, not increment
            self.pbar.n = min(current_seconds, self.pbar.total)
            self.pbar.refresh()
        
        # Optional: If you still want to see the text logs below the bar, uncomment this:
        # self.terminal.write(message) 

    def flush(self):
        self.terminal.flush()

    def close(self):
        self.pbar.close()

def transcribe_video():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename> [model_name]")
        sys.exit(1)

    input_file = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    print(f"--- Initialization ---")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device.upper()}")

    # 1. Get Duration
    duration = get_duration(input_file)
    if duration:
        print(f"Media Duration: {duration:.2f} seconds")
    else:
        print("Warning: Could not detect duration. Progress bar will not show percentage.")

    # 2. Load Model
    print(f"Loading '{model_name}' model...")
    model = whisper.load_model(model_name, device=device)

    # 3. Transcribe with Progress Bar
    print("--- Starting Transcription ---")
    
    # Redirect stdout to our custom parser if we have a duration
    original_stdout = sys.stdout
    if duration:
        progress_tracker = ProgressOutput(duration)
        sys.stdout = progress_tracker

    try:
        # verbose=True forces Whisper to print timestamps to stdout
        result = model.transcribe(input_file, verbose=True)
    finally:
        # Restore stdout and close bar
        if duration:
            sys.stdout = original_stdout
            progress_tracker.close()

    # 4. Save Output
    output_filename = os.path.splitext(input_file)[0] + ".txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"\nDone! Saved to: {output_filename}")

if __name__ == "__main__":
    transcribe_video()