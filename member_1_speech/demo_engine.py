import pyaudio
import wave
import whisper
import os
import warnings

# Suppress minor warnings to keep the terminal output clean
warnings.filterwarnings("ignore", category=UserWarning)

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "temp_recording.wav"

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("\n" + "="*50)
    print("  LISTENING (Speak for 5 seconds...)")
    print("="*50)
    
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    print("⏹️  Processing audio...")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save temporarily for Whisper to read
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def detect_intent(text):
    text = text.lower().strip()
    
    # Check for presentation commands
    if "next slide" in text or "moving on" in text:
        return "⏭️  ACTION: NEXT_SLIDE"
    elif "previous slide" in text or "go back" in text:
        return "⏮️  ACTION: PREVIOUS_SLIDE"
    elif "for example" in text or "as an example" in text:
        return "🔍 ACTION: ZOOM_EXAMPLE"
    elif "highlight" in text:
        words = text.split()
        try:
            target_word = words[words.index("highlight") + 1]
            return f"🖍️  ACTION: HIGHLIGHT (Word: '{target_word}')"
        except (ValueError, IndexError):
            return "🖍️  ACTION: HIGHLIGHT (No specific word detected)"
    
    return "⏳ (Normal speech detected. No slide action taken.)"

def run_demo():
    print("🚀 Initializing Voice Presentation Assistant...")
    print("🧠 Loading AI Model (this takes a few seconds)...")
    
    # Load the Whisper AI model
    model = whisper.load_model("base")
    print("✅ System Ready!\n")
    
    try:
        while True:
            input(" Press [ENTER] when you are ready to speak (or press Ctrl+C to quit)...")
            record_audio()
            
            # 1. Transcribe the audio
            result = model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False)
            spoken_text = result["text"].strip()
            
            print(f"\n🗣️  You said: '{spoken_text}'")
            
            # 2. Detect the intent
            action = detect_intent(spoken_text)
            print(f"🤖 System Decision: {action}\n")
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Demo. Great job!")
        # Clean up the temporary audio file
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            os.remove(WAVE_OUTPUT_FILENAME)

if __name__ == "__main__":
    run_demo()