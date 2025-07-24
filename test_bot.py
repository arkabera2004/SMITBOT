#!/usr/bin/env python3
"""
Test script to verify all components are working
"""

import sys
import subprocess

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ ollama import failed: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test Ollama connection and model availability"""
    print("\nTesting Ollama connection...")
    
    try:
        import ollama
        
        # Test connection
        models = ollama.list()
        print("✅ Ollama connection successful")
        
        # Check available models
        model_names = [model.model for model in models.models]
        print(f"Available models: {model_names}")
        
        # Check if gemma3:latest is available
        if 'gemma3:latest' in model_names:
            print("✅ Gemma3 model is available")
        else:
            print("❌ Gemma3 model not found. Available models:", model_names)
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("Make sure Ollama is running: ollama serve")
        return False

def test_audio_devices():
    """Test audio input/output devices"""
    print("\nTesting audio devices...")
    
    try:
        import speech_recognition as sr
        import pyttsx3
        
        # Test microphone
        recognizer = sr.Recognizer()
        microphones = sr.Microphone.list_microphone_names()
        
        if microphones:
            print(f"✅ Found {len(microphones)} microphone(s)")
            print(f"Default microphone: {microphones[0] if microphones else 'None'}")
        else:
            print("❌ No microphones found")
            return False
        
        # Test TTS engine
        tts_engine = pyttsx3.init()
        voices = tts_engine.getProperty('voices')
        
        if voices:
            print(f"✅ Found {len(voices)} voice(s) for TTS")
        else:
            print("⚠️ No TTS voices found (may still work)")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_simple_conversation():
    """Test a simple conversation with the bot"""
    print("\nTesting simple conversation...")
    
    try:
        import sys
        import os
        
        # Add the ollama-bot src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'ollama-bot', 'src'))
        
        from bot.ollama_client import OllamaClient
        
        # Initialize client
        client = OllamaClient(model_name="gemma3:latest")
        
        # Test simple query
        response = client.send_query("Hello, can you hear me?")
        
        if response and len(response) > 0:
            print("✅ Simple conversation test passed")
            print(f"Bot response: {response[:100]}...")
            return True
        else:
            print("❌ Empty response from bot")
            return False
            
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Voice-to-Voice Bot Test Suite ===\n")
    
    tests = [
        test_imports,
        test_ollama_connection,
        test_audio_devices,
        test_simple_conversation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print("-" * 50)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All tests passed! The bot should work correctly.")
        print("\nYou can now run:")
        print("  python3 voice2voice.py")
        print("  or")
        print("  cd ollama-bot/src && python3 main.py")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip3 install -r requirements.txt")
        print("2. Start Ollama: ollama serve")
        print("3. Download model: ollama pull gemma2")
        print("4. Check microphone permissions")

if __name__ == "__main__":
    main()
