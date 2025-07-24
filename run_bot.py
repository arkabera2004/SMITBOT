#!/usr/bin/env python3
"""
Quick launcher script for the Voice-to-Voice Bot
"""

import os
import sys
import subprocess

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def main():
    print("=== ARKA Launcher ===")
    print("Your friendly 25-year-old Indian voice assistant!")
    
    # Check if Ollama is running
    if not check_ollama():
        print("❌ Ollama is not running or not installed.")
        print("Please run: ollama serve")
        print("Or install Ollama from: https://ollama.ai/")
        return
    
    print("✅ Ollama is running")
    
    # Show options
    print("\nChoose how you want to chat with ARKA:")
    print("1. Pure Voice Mode (voice2voice.py) - Talk directly to ARKA")
    print("2. Enhanced Mode (ollama-bot) - Text and voice options")
    print("3. Test ARKA's voice")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\nStarting ARKA in pure voice mode...")
            print("Get ready to chat with your Indian friend!")
            os.system("python3 voice2voice.py")
            break
        elif choice == '2':
            print("\nStarting ARKA in enhanced mode...")
            os.chdir("ollama-bot/src")
            os.system("python3 main.py")
            break
        elif choice == '3':
            print("\nTesting ARKA's voice...")
            os.system("python3 test_arka.py")
            break
        elif choice == '4':
            print("See you later, yaar!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
