import whisper
import sys
import os
import argparse

def transcribe_video(video_path, model_size="medium"):
    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing '{video_path}' in Hebrew...")
    # task="transcribe" acts as default, language="he" forces Hebrew
    result = model.transcribe(video_path, language="he", verbose=True)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_txt = f"{base_name}_transcript.txt"
    output_srt = f"{base_name}_transcript.srt"

    # Save as plain text
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    # Simple SRT formatter (Whisper CLI does this better, but this works for basic custom script)
    # Note: result['segments'] contains timestamps if we want to write SRT manually.
    # For now, let's stick to simple text as requested, but I'll add segments dump to text for reference.
    
    print(f"Transcription complete. Saved to {output_txt}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe video to Hebrew using Whisper")
    parser.add_argument("video_file", help="Path to the video file to transcribe")
    parser.add_argument("--model", default="medium", help="Whisper model size (tiny, base, small, medium, large)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video_file):
        print(f"Error: File '{args.video_file}' not found.")
        sys.exit(1)

    transcribe_video(args.video_file, args.model)
