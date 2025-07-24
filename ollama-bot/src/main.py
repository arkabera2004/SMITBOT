# filepath: /ollama-bot/ollama-bot/src/main.py

import os
import sys
from bot.ollama_client import OllamaClient
from bot.conversation import Conversation

def main():
    """Main function to run ARKA - the Indian voice assistant"""
    print("=== ARKA - Your Indian Voice Assistant ===")
    print("A friendly 25-year-old Indian guy ready to chat!")
    print("Make sure Ollama is installed and running!")
    print("Available modes: text and voice interaction\n")
    
    try:
        # Load environment variables
        load_env_variables()

        # Initialize the Ollama client with the Gemma3 model
        print("Initializing ARKA...")
        ollama_client = OllamaClient(model_name="gemma3:latest")

        # Start the conversation loop
        conversation = Conversation(ollama_client)
        conversation.start()
        
    except KeyboardInterrupt:
        print("\nGoodbye from ARKA!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def load_env_variables():
    """Load environment variables from .env file"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not installed. Skipping .env file loading.")
    except Exception as e:
        print(f"Error loading environment variables: {e}")

if __name__ == "__main__":
    main()