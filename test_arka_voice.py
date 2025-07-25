#!/usr/bin/env python3
"""
Simple test to verify ARKA's voice output is working
"""

import pyttsx3
import time

def test_voice_output():
    print("=== Testing ARKA's Voice Output ===")
    
    # Initialize TTS engine
    engine = pyttsx3.init()
    
    # Configure like ARKA
    voices = engine.getProperty('voices')
    daniel_voice = None
    for voice in voices:
        if 'daniel' in voice.name.lower():
            daniel_voice = voice
            break
    
    if daniel_voice:
        engine.setProperty('voice', daniel_voice.id)
        print(f"Using Daniel voice: {daniel_voice.name}")
    
    engine.setProperty('rate', 155)
    engine.setProperty('volume', 0.9)
    
    # Test messages
    test_messages = [
        "Hello! This is ARKA speaking.",
        "Hey there, yaar! Can you hear me clearly?",
        "I'm testing my voice output to make sure everything is working perfectly!",
        "If you can hear this, then my text-to-speech system is working correctly!"
    ]
    
    print("\n🔊 You should hear ARKA speaking now...")
    print("If you don't hear anything, check your:")
    print("1. System volume")
    print("2. Speaker/headphone connection")
    print("3. Audio output device selection")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        engine.say(message)
        engine.runAndWait()
        time.sleep(0.5)  # Brief pause between tests
    
    print("\n✅ Voice test completed!")
    print("If you heard all 4 messages clearly, ARKA's voice is working perfectly!")
    print("If you didn't hear anything, there might be an audio system issue.")

if __name__ == "__main__":
    test_voice_output()
