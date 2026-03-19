# audio/mic_test.py - Lists all functional audio input devices
import pyaudio

def list_microphones():
    # 1. Initialize PyAudio
    # This creates an object that communicates with your computer's sound system
    audio_manager = pyaudio.PyAudio()

    print("Searching for audio input devices...\n")

    # 2. Get the total number of audio devices connected to the computer
    # This includes speakers, microphones, and virtual drivers
    device_count = audio_manager.get_device_count()

    print(f"Found {device_count} total audio devices. Filtering for inputs...\n")
    print(f"{'ID':<5} {'Device Name'}")
    print("-" * 30)

    # 3. Loop through every device found
    for i in range(device_count):
        device_info = audio_manager.get_device_info_by_index(i)

        # 4. Check if the device supports input
        # 'maxInputChannels' > 0 means the device can record sound
        if device_info.get('maxInputChannels') > 0:
            device_name = device_info.get('name')
            print(f"{i:<5} {device_name}")

    # 5. Clean up
    # Always terminate the PyAudio object to free up system resources
    audio_manager.terminate()
    print("\nSearch complete. Use the ID number to select a mic in your project.")

if __name__ == "__main__":
    list_microphones()