# audio/silence_detector.py - Simple threshold-based silence detection
import numpy as np

# A threshold value. You might need to adjust this depending on your mic.
# Higher = more aggressive silence detection.
SILENCE_THRESHOLD = 500 

def is_silent(audio_data):
    """
    Checks if the provided audio data is 'silent'.
    audio_data: raw bytes from PyAudio
    """
    
    # 1. Convert the raw bytes into a format Python can do math with (16-bit integers)
    # This creates a 'list' of numbers representing the sound wave.
    audio_as_numbers = np.frombuffer(audio_data, dtype=np.int16)
    
    # 2. Calculate the 'Energy' or Volume.
    # We take the average of the absolute values of all samples.
    # Absolute values are used because sound waves go positive and negative.
    average_volume = np.abs(audio_as_numbers).mean()
    
    # 3. Compare the volume to our threshold
    if average_volume < SILENCE_THRESHOLD:
        return True
    else:
        return False

# Example usage (for testing)
if __name__ == "__main__":
    print("Silence detector module loaded.")
    print(f"Current threshold: {SILENCE_THRESHOLD}")