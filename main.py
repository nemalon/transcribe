import sys
import os
import whisper

def transcribe_video():
    """
    Transcribes a video or audio file using the Whisper model.
    The filename is expected as the first argument.
    """
    if len(sys.argv) < 2:
        print("Error: No video filename provided.")
        print("Usage: python main.py <filename> [model_name]")
        sys.exit(1)

    input_file = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    # Check if the file exists within the mounted volume (/app)
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'. Ensure it is in the mounted directory.")
        sys.exit(1)

    print(f"--- Starting Transcription ---")
    print(f"File: {input_file}")
    print(f"Model: {model_name} (Using GPU if available)")

    try:
        # Load the model. Whisper automatically detects and uses the GPU.
        model = whisper.load_model(model_name)
        
        # Perform the transcription
        result = model.transcribe(input_file)
        
        output_filename = os.path.splitext(input_file)[0] + ".txt"
        
        # Write the transcription to a new file in the mounted directory (/app)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print("--- Transcription Complete ---")
        print(f"Output saved to: {output_filename}")

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        sys.exit(1)

if __name__ == "__main__":
    transcribe_video()