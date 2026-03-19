import whisper
import pyaudio
import numpy as np
import wave
import warnings
import gc # Added for memory management
from intent_detection import detect_intent

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

class SpeechEngine:
    def __init__(self):
        print("Initializing Whisper AI Engine...")
        self.model = whisper.load_model("base")
        self.temp_file = "input_cache.wav"

    def process_audio(self, duration=2.5):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                        input=True, frames_per_buffer=2048)
        
        print("Listening for input...")
        frames = []
        try:
            for _ in range(0, int(16000 / 2048 * duration)):
                # Added 'exception_on_overflow=False' to stop crashes
                data = stream.read(2048, exception_on_overflow=False)
                frames.append(data)
        finally:
            # Explicit cleanup to prevent hardware sticking
            stream.stop_stream()
            stream.close()
            p.terminate()

        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        audio_data = (audio_data * 2.8).clip(-32768, 32767).astype(np.int16)

        with wave.open(self.temp_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data.tobytes())

        result = self.model.transcribe(self.temp_file, fp16=False, language="en")
        transcription = result["text"].strip()
        
        # Force memory cleanup after AI processing
        gc.collect() 
        
        return {
            "text": transcription, 
            "intent": detect_intent(transcription)
        }