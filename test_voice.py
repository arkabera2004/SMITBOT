#!/usr/bin/env python3
"""
Voice Test Script - Test the natural voice improvements
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ollama-bot', 'src'))

import pyttsx3
import time

def test_voice_improvements():
    """Test the improved natural voice settings"""
    print("=== Voice Improvement Test ===")
    
    # Initialize TTS engine
    tts_engine = pyttsx3.init()
    
    # Configure for natural voice
    voices = tts_engine.getProperty('voices')
    
    # Try to find the most natural sounding voice
    best_voice = None
    preferred_voices = [
        'samantha', 'alex', 'victoria', 'allison', 'ava', 'susan', 'karen',
        'tessa', 'veena', 'fiona', 'moira', 'nicky', 'emily', 'kate'
    ]
    
    if voices:
        print(f"Available voices: {len(voices)}")
        
        # First try to find preferred natural voices
        for voice in voices:
            voice_name = voice.name.lower()
            for preferred in preferred_voices:
                if preferred in voice_name:
                    best_voice = voice
                    break
            if best_voice:
                break
        
        # If no preferred voice found, try to find any natural voice
        if not best_voice:
            for voice in voices:
                if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'samantha', 'alex']):
                    best_voice = voice
                    break
        
        # Use the best voice found
        if best_voice:
            tts_engine.setProperty('voice', best_voice.id)
            print(f"Selected voice: {best_voice.name}")
        elif voices:
            tts_engine.setProperty('voice', voices[0].id)
            print(f"Using default voice: {voices[0].name}")
    
    # Set natural speech parameters
    tts_engine.setProperty('rate', 160)    # Slower, more natural speed
    tts_engine.setProperty('volume', 0.8)  # Slightly softer volume
    
    print("\n=== Testing Natural Speech ===")
    
    # Test messages with different natural speech patterns
    test_messages = [
        "Hey there! I'm your new voice assistant, and I'm really excited to chat with you today.",
        "You know, I think this conversation is going to be great. I'm here to help with whatever you need!",
        "Actually, I've been upgraded to sound more natural and conversational. What do you think?",
        "Well, I'd love to hear about what you're working on. I'm genuinely curious about your projects!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        input("Press Enter to hear this message...")
        
        # Speak with natural pauses
        sentences = message.split('. ')
        for j, sentence in enumerate(sentences):
            if sentence.strip():
                # Add period back if it was removed by split
                if j < len(sentences) - 1:
                    sentence += '.'
                
                tts_engine.say(sentence.strip())
                tts_engine.runAndWait()
                
                # Small pause between sentences for natural flow
                if j < len(sentences) - 1:
                    time.sleep(0.3)
    
    print("\n=== Voice Test Complete ===")
    print("The voice should now sound more natural and conversational!")

if __name__ == "__main__":
    test_voice_improvements()
