import whisper
import os

def test_transcription():
    filepath = os.path.join("audio_samples", "test_chunk.wav")
    
    if not os.path.exists(filepath):
        print(f"❌ Error: {filepath} not found. Run 02_record_audio.py first!")
        return

    print("🧠 Loading Whisper model ('base')...")
    model = whisper.load_model("base") 

    print(f"🎧 Transcribing {filepath}...")
    result = model.transcribe(filepath, fp16=False)
    
    print("\n📝 Transcription Result:")
    print("-" * 30)
    print(result["text"].strip())
    print("-" * 30)

if __name__ == "__main__":
    test_transcription()