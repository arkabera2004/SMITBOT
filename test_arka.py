#!/usr/bin/env python3
"""
ARKA Voice Test Script - Test the Indian male voice assistant
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ollama-bot', 'src'))

import pyttsx3
import time

def test_arka_voice():
    """Test ARKA's voice improvements"""
    print("=== ARKA Voice Test ===")
    print("Testing the voice of a 25-year-old Indian guy named ARKA")
    
    # Initialize TTS engine
    tts_engine = pyttsx3.init()
    
    # Configure for Indian male voice
    voices = tts_engine.getProperty('voices')
    
    # Try to find the best male voice
    best_voice = None
    preferred_male_voices = [
        'ravi', 'ajay', 'aaron', 'alex', 'daniel', 'fred', 'jorge', 'diego',
        'carlos', 'junior', 'lee', 'luca', 'magnus', 'martin', 'nicolas',
        'oliver', 'ralph', 'thomas', 'viktor', 'winston', 'yannick'
    ]
    
    if voices:
        print(f"Searching through {len(voices)} available voices for best male voice...")
        
        # First try to find preferred male voices
        for voice in voices:
            voice_name = voice.name.lower()
            for preferred in preferred_male_voices:
                if preferred in voice_name:
                    best_voice = voice
                    break
            if best_voice:
                break
        
        # If no preferred voice found, try to find any male voice
        if not best_voice:
            for voice in voices:
                voice_name = voice.name.lower()
                if any(keyword in voice_name for keyword in ['male', 'man', 'alex', 'daniel', 'aaron']):
                    best_voice = voice
                    break
        
        # Use the best voice found
        if best_voice:
            tts_engine.setProperty('voice', best_voice.id)
            print(f"ARKA using voice: {best_voice.name}")
        elif voices:
            tts_engine.setProperty('voice', voices[0].id)
            print(f"ARKA using default voice: {voices[0].name}")
    
    # Set natural speech parameters for a 25-year-old Indian male
    tts_engine.setProperty('rate', 155)    # Slightly faster, energetic pace
    tts_engine.setProperty('volume', 0.85) # Clear, confident volume
    
    print("\n=== Testing ARKA's Natural Indian Speech ===")
    
    # Test messages with ARKA's personality
    test_messages = [
        "Hey there! I'm ARKA, your friendly voice assistant! I'm really excited to chat with you today, yaar!",
        "Actually, I'm a 25-year-old Indian guy who's totally passionate about helping people with their questions and tasks.",
        "You know what, I think we're going to have an awesome conversation! What would you like to talk about today?",
        "Basically, I'm here to help with whatever you need, yaar. Whether it's answering questions, helping with work, or just having a friendly chat!",
        "That's totally cool! I love meeting new people and learning about what they're working on. It's really interesting!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        input("Press Enter to hear ARKA say this...")
        
        # Speak with natural pauses like ARKA
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
                    time.sleep(0.2)
    
    print("\n=== ARKA Voice Test Complete ===")
    print("ARKA should now sound like a friendly 25-year-old Indian guy!")
    print("Ready to chat with his natural, enthusiastic personality!")

if __name__ == "__main__":
    test_arka_voice()
