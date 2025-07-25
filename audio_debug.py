#!/usr/bin/env python3
"""
ARKA Voice Assistant - Audio Troubleshooting Version
This version includes enhanced audio debugging and fallback options
"""

import pyttsx3
import subprocess
import sys
import os

def check_system_audio():
    """Check if system audio is working"""
    print("🔊 Testing system audio...")
    try:
        # Test with macOS 'say' command
        subprocess.run(['say', 'System audio test'], check=True, timeout=5)
        print("✅ System audio is working!")
        return True
    except:
        print("❌ System audio might have issues")
        return False

def check_pyttsx3_audio():
    """Check if pyttsx3 audio is working"""
    print("🔊 Testing pyttsx3 audio...")
    try:
        engine = pyttsx3.init()
        engine.setProperty('volume', 1.0)  # Max volume
        engine.setProperty('rate', 150)
        
        # Test with Daniel voice
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'daniel' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.say("pyttsx3 audio test")
        engine.runAndWait()
        print("✅ pyttsx3 audio is working!")
        return True
    except Exception as e:
        print(f"❌ pyttsx3 audio error: {e}")
        return False

def main():
    print("=== ARKA Audio Troubleshooting ===\n")
    
    # Check system volume
    print("📱 Checking system setup...")
    print("1. Make sure your volume is turned up")
    print("2. Check that the correct audio output device is selected")
    print("3. Ensure no other apps are using exclusive audio access\n")
    
    # Test system audio
    system_ok = check_system_audio()
    print()
    
    # Test pyttsx3 audio
    pyttsx3_ok = check_pyttsx3_audio()
    print()
    
    if system_ok and pyttsx3_ok:
        print("🎉 All audio systems are working!")
        print("ARKA should be able to speak to you properly.")
        print("\nIf you still can't hear ARKA, try:")
        print("- Restart the Terminal app")
        print("- Check macOS Privacy & Security settings for microphone/audio")
        print("- Try using headphones instead of speakers")
    elif system_ok and not pyttsx3_ok:
        print("⚠️  System audio works but pyttsx3 has issues")
        print("This might be a Python audio library problem")
    elif not system_ok:
        print("❌ System audio issues detected")
        print("Check your Mac's audio settings and hardware")
    
    print(f"\n🔧 Audio debugging complete!")

if __name__ == "__main__":
    main()
