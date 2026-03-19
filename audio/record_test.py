# audio/record_test.py - Records 2 seconds of audio to a file
import pyaudio
import wave

# Settings for the recording
FORMAT = pyaudio.paInt16  # Standard 16-bit resolution
CHANNELS = 1              # Mono (1 channel)
RATE = 16000             # Sample rate in Hz
CHUNK = 1024              # Size of each data "packet" read from the mic
RECORD_SECONDS = 2        # Duration
OUTPUT_FILENAME = "audio/output.wav"

def record_audio():
    audio_manager = pyaudio.PyAudio()

    # 1. Open the "stream" (the connection to your microphone)
    stream = audio_manager.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

    print("Recording started...")

    frames = []

    # 2. Loop to capture audio data in small chunks
    # We calculate how many chunks are needed for 2 seconds
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # 3. Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio_manager.terminate()

    # 4. Save the raw data as a WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_manager.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"File saved as: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    record_audio()