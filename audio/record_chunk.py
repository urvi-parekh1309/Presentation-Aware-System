# audio/record_chunk.py - Records audio in-memory and checks for silence
import pyaudio
import time

# Import your own silence detector!
from silence_detector import is_silent 

# Assuming you have a function in speech_to_text.py that accepts raw audio data:
# from speech.speech_to_text import transcribe_audio 

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2 

def get_single_chunk(audio_manager):
    """Records a single 2-second burst of audio and returns it in memory."""
    stream = audio_manager.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

    print("Listening...")
    frames = []

    # Capture data for the specified duration
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream for this specific chunk
    stream.stop_stream()
    stream.close()

    # Combine all the little packets into one big block of audio bytes (IN MEMORY)
    raw_audio_bytes = b''.join(frames)
    
    return raw_audio_bytes

def main():
    audio_manager = pyaudio.PyAudio()
    
    try:
        print("Starting continuous listening... Press Ctrl+C to stop.")
        
        # Changed to a continuous loop instead of just 3 chunks
        while True: 
            # 1. Capture the audio directly into RAM
            audio_data = get_single_chunk(audio_manager)
            
            # 2. Check if the chunk is just background noise
            if is_silent(audio_data):
                print("Silence detected, skipping...")
                continue # Skip the rest of the loop and listen again immediately
                
            print("Sound detected! Sending to speech-to-text...")
            
            # 3. Pass the in-memory data to your speech-to-text engine
            # text_output = transcribe_audio(audio_data)
            # print(f"You said: {text_output}")
            
            # Optional: a tiny pause between recordings
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")
    finally:
        audio_manager.terminate()
        print("\nMicrophone released. Goodbye!")

if __name__ == "__main__":
    main()