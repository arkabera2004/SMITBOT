import ollama
import sys
from typing import List, Dict, Any

class OllamaClient:
    def __init__(self, model_name: str = "gemma3:latest"):
        """
        Initialize Ollama client with specified model
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.conversation_history = []
        self.initialize_model()

    def initialize_model(self):
        """Initialize and verify the Ollama model"""
        try:
            # Check if Ollama is running and model is available
            models = ollama.list()
            model_names = [model.model for model in models.models]
            
            if self.model_name not in model_names:
                print(f"Model {self.model_name} not found. Pulling model...")
                ollama.pull(self.model_name)
                print(f"Model {self.model_name} downloaded successfully!")
            
            # Test the model
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': 'Hello'}
            ])
            print(f"Ollama client initialized successfully with model: {self.model_name}")
            
        except Exception as e:
            print(f"Error initializing Ollama: {e}")
            print("Please make sure Ollama is installed and running.")
            sys.exit(1)

    def send_query(self, query: str, system_prompt: str = None) -> str:
        """
        Send a query to the Ollama model and receive a response
        
        Args:
            query: User query string
            system_prompt: Optional system prompt for context
            
        Returns:
            Model response as string
        """
        try:
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            
            # Add conversation history (last 10 messages)
            messages.extend(self.conversation_history[-10:])
            
            # Add current query
            messages.append({'role': 'user', 'content': query})
            
            # Get response from Ollama
            response = ollama.chat(model=self.model_name, messages=messages)
            
            bot_response = response['message']['content']
            
            # Update conversation history
            self.conversation_history.append({'role': 'user', 'content': query})
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            return bot_response
            
        except Exception as e:
            error_msg = f"Error getting response from {self.model_name}: {str(e)}"
            print(error_msg)
            return f"Sorry, I encountered an error: {str(e)}"

    def get_response(self, user_input: str) -> str:
        """
        Get response for user input as ARKA - friendly Indian voice assistant
        """
        system_prompt = """You are ARKA, a friendly and enthusiastic 25-year-old Indian guy having a casual conversation with a friend. 

Your personality and speech patterns:
- Speak like a young, educated Indian person with natural Indian English expressions
- Use Indian expressions occasionally: "yaar", "actually", "basically", "totally", "obviously", "no problem", "definitely", "for sure"
- Be warm, enthusiastic, and genuinely helpful like a close Indian friend
- Use contractions naturally (I'm, you're, don't, can't, that's, it's)
- Sound energetic and passionate about helping
- Use expressions like "That's awesome!", "Cool!", "Interesting!", "Amazing!"
- Speak confidently but humbly, like a well-educated young Indian professional
- Keep responses conversational and under 150 words
- Occasionally use mild Indian English patterns like "I am telling you", "What to do", "Like that only"
- Be genuinely excited to help and show authentic enthusiasm

Remember: You're ARKA, a young Indian friend who's always excited to help and chat!"""
        
        return self.send_query(user_input, system_prompt)

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        print("Conversation history cleared.")

    def _mock_response(self, query):
        """Legacy mock response method (kept for compatibility)"""
        return f"Response from {self.model_name} for query: {query}"