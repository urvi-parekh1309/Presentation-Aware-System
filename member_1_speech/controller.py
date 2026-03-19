import pyautogui
import time
import os
from speech_engine import SpeechEngine

def main():
    if os.path.exists("input_cache.wav"):
        try:
            os.remove("input_cache.wav")
        except:
            pass

    engine = SpeechEngine()
    print("Presentation System Online.")
    print("Ready for voice commands.")
    print("-------------------------")

    try:
        while True:
            data = engine.process_audio()
            action = data['intent']['action']
            
            if len(data['text']) > 1:
                print(f"Recognized: {data['text']}")

            # Immediate execution with a safety buffer
            if action == "PREVIOUS_SLIDE":
                print("Action: Previous")
                pyautogui.press('left')
                time.sleep(1.0) # Buffer to let the OS catch up
                
            elif action == "NEXT_SLIDE":
                print("Action: Next")
                pyautogui.press('right')
                time.sleep(1.0)
                
            elif action == "ZOOM_IN":
                print("Action: Zoom")
                pyautogui.hotkey('ctrl', '=')
                time.sleep(3.0)
                pyautogui.hotkey('ctrl', '0')
            
            # Small global pause to prevent CPU spike
            time.sleep(0.2)
                
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()