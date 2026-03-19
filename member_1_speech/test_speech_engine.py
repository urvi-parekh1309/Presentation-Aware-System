from speech_engine import SpeechEngine

def start_demo():
    # Initialize our AI Engine
    engine = SpeechEngine()
    print("\n✅ System Online! Presentation Assistant is ready.")
    print("-" * 50)
    
    try:
        while True:
            print("\n👉 Press Enter to start speaking (or Ctrl+C to stop)...")
            input() 
            
            data = engine.process_speech(seconds=5)
            
            print(f"\n🗣️  You said: '{data['text']}'")
            print(f"🤖 Action: {data['intent']['action']}")
            
            if data['intent']['target_word']:
                print(f"🎯 Target Word: {data['intent']['target_word']}")
            print("-" * 30)
                
    except KeyboardInterrupt:
        print("\n\n👋 Demo Stopped. Great work today!")

if __name__ == "__main__":
    start_demo()