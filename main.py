import sys
import os
import re
import subprocess
import whisper
import torch
from tqdm import tqdm
from whisper.utils import get_writer  # <--- NEW IMPORT

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
        self.terminal = sys.stdout 

    def write(self, message):
        match = TIMESTAMP_PATTERN.search(message)
        if match:
            current_time_str = match.group(1)
            current_seconds = parse_timestamp_to_seconds(current_time_str)
            self.pbar.n = min(current_seconds, self.pbar.total)
            self.pbar.refresh()

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

    duration = get_duration(input_file)
    if duration:
        print(f"Media Duration: {duration:.2f} seconds")

    print(f"Loading '{model_name}' model...")
    model = whisper.load_model(model_name, device=device)

    print("--- Starting Transcription ---")
    
    original_stdout = sys.stdout
    if duration:
        progress_tracker = ProgressOutput(duration)
        sys.stdout = progress_tracker

    try:
        # We assume the user wants verbose=True for the progress bar to work
        result = model.transcribe(input_file, verbose=True)
    finally:
        if duration:
            sys.stdout = original_stdout
            progress_tracker.close()

    # --- 5. Save Output (TXT and SRT) ---
    output_dir = os.path.dirname(input_file) or "."
    
    # Define the formats we want to save
    output_formats = ["txt", "srt"]
    
    print(f"\n--- Saving Files ---")
    
    for fmt in output_formats:
        # Get the appropriate writer function (WriteTXT, WriteSRT, etc.)
        writer = get_writer(fmt, output_dir)
        
        # Save the file
        # 'input_file' argument is used to name the output file (e.g., video.mp4 -> video.srt)
        writer(result, input_file)
        print(f"Saved: {os.path.splitext(input_file)[0]}.{fmt}")

    print("--- Done ---")

if __name__ == "__main__":
    transcribe_video()