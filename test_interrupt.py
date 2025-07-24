#!/usr/bin/env python3
"""
Test script for ARKA's interrupt detection feature
"""

import pyttsx3
import time
import threading

def test_interrupt_simulation():
    """Simulate the interrupt functionality"""
    print("=== ARKA Interrupt Detection Test ===")
    print("This simulates how ARKA will stop talking when you interrupt")
    
    # Initialize TTS engine
    tts_engine = pyttsx3.init()
    
    # Configure voice like ARKA
    voices = tts_engine.getProperty('voices')
    if voices:
        for voice in voices:
            if 'daniel' in voice.name.lower():
                tts_engine.setProperty('voice', voice.id)
                break
    
    tts_engine.setProperty('rate', 155)
    tts_engine.setProperty('volume', 0.85)
    
    # Test messages
    long_message = """Hey there, yaar! I'm ARKA and I'm really excited to tell you about this amazing new feature. 
    Actually, now I can detect when you want to interrupt me while I'm speaking. 
    Basically, this means our conversation will be much more natural and responsive. 
    You don't have to wait for me to finish my entire response. 
    You can just start talking whenever you want, and I'll immediately stop and listen to you!"""
    
    print("\nARKA will now speak a long message.")
    print("In real usage, you could interrupt him by speaking.")
    print("For this demo, press Enter after a few seconds to simulate an interrupt.\n")
    
    # Simulate speaking with interrupt detection
    should_stop = False
    
    def check_for_interrupt():
        nonlocal should_stop
        input("Press Enter to simulate interrupting ARKA...")
        should_stop = True
        print("\n🛑 INTERRUPT DETECTED! ARKA stops speaking and listens...")
    
    # Start interrupt detection thread
    interrupt_thread = threading.Thread(target=check_for_interrupt, daemon=True)
    interrupt_thread.start()
    
    # Speak with interrupt capability
    sentences = long_message.split('. ')
    
    print("ARKA: ", end="", flush=True)
    
    for i, sentence in enumerate(sentences):
        if sentence.strip() and not should_stop:
            if i < len(sentences) - 1:
                sentence += '.'
            
            print(f"{sentence.strip()}", end=" ", flush=True)
            
            # Simulate TTS speaking (in real version, this monitors tts_engine.isBusy())
            start_time = time.time()
            while time.time() - start_time < 2.0 and not should_stop:  # 2 seconds per sentence
                time.sleep(0.1)
            
            if should_stop:
                print("\n\n✅ ARKA successfully stopped speaking!")
                print("Now ARKA would listen to your interrupt and respond accordingly.")
                break
            
            # Pause between sentences
            if i < len(sentences) - 1:
                time.sleep(0.3)
    
    if not should_stop:
        print("\n\nARKA finished speaking without interruption.")
    
    print("\n=== Interrupt Test Complete ===")
    print("In real usage:")
    print("✅ Just start speaking while ARKA is talking")
    print("✅ ARKA will immediately stop and listen")
    print("✅ Your interrupt will be processed and responded to")
    print("✅ Much more natural conversation flow!")

if __name__ == "__main__":
    test_interrupt_simulation()
