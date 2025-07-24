#!/usr/bin/env python3
"""
Voice-to-Voice Bot using Ollama Gemma 3 Model
An offline bot that speaks with users, understands requirements, and replies based on queries.
"""

import speech_recognition as sr
import pyttsx3
import ollama
import threading
import queue
import time
import sys
import re
from typing import Optional, Dict, Any

class VoiceToVoiceBot:
    def __init__(self, model_name: str = "gemma3:latest"):
        """
        Initialize the Voice-to-Voice Bot
        
        Args:
            model_name: Name of the Ollama model to use (default: gemma3:latest)
        """
        self.model_name = model_name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.conversation_history = []
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Configure TTS settings
        self._configure_tts()
        
        # Test Ollama connection
        self._test_ollama_connection()
        
        print(f"Voice-to-Voice Bot initialized with model: {self.model_name}")
        print("Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("ARKA is ready to chat!")

    def _configure_tts(self):
        """Configure Text-to-Speech settings for natural Indian male voice"""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find the best male voice that can simulate Indian accent
        best_voice = None
        
        # Preferred male voices (prioritizing deeper, more masculine voices)
        preferred_male_voices = [
            'ravi', 'ajay', 'aaron', 'alex', 'daniel', 'fred', 'jorge', 'diego',
            'carlos', 'junior', 'lee', 'luca', 'magnus', 'martin', 'milena', 'nicolas',
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
                    # Look for male indicators
                    if any(keyword in voice_name for keyword in ['male', 'man', 'alex', 'daniel', 'aaron', 'fred']):
                        best_voice = voice
                        break
            
            # If still no male voice found, look for neutral/deeper voices
            if not best_voice:
                for voice in voices:
                    voice_name = voice.name.lower()
                    # Avoid obviously female voices
                    if not any(keyword in voice_name for keyword in ['female', 'woman', 'girl', 'samantha', 'victoria', 'allison', 'ava', 'susan', 'karen']):
                        best_voice = voice
                        break
            
            # Use the best voice found, or default to first available
            if best_voice:
                self.tts_engine.setProperty('voice', best_voice.id)
                print(f"ARKA using voice: {best_voice.name}")
            elif voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                print(f"ARKA using default voice: {voices[0].name}")
        
        # Set natural speech parameters for a 25-year-old Indian male
        self.tts_engine.setProperty('rate', 155)    # Slightly faster, energetic pace
        self.tts_engine.setProperty('volume', 0.85) # Clear, confident volume
        
        # Try to set additional properties for more natural speech
        try:
            # Slightly lower pitch for male voice
            self.tts_engine.setProperty('pitch', -0.1)
            # More inflection for expressive Indian English
            self.tts_engine.setProperty('inflection', 0.15)
        except:
            pass  # Ignore if properties not supported

    def _test_ollama_connection(self):
        """Test connection to Ollama and pull model if needed"""
        try:
            # Check if model is available
            models = ollama.list()
            model_names = [model.model for model in models.models]
            
            if self.model_name not in model_names:
                print(f"Model {self.model_name} not found. Pulling model...")
                self.speak(f"Downloading {self.model_name} model. This may take a while...")
                ollama.pull(self.model_name)
                print(f"Model {self.model_name} downloaded successfully!")
            
            # Test the model with a simple query
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': 'Hello, can you hear me?'}
            ])
            print("Ollama connection successful!")
            
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("Please make sure Ollama is installed and running.")
            sys.exit(1)

    def speak(self, text: str):
        """Convert text to speech with natural pauses"""
        print(f"Bot: {text}")
        
        # Add natural pauses for better speech flow
        sentences = text.split('. ')
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                # Add period back if it was removed by split
                if i < len(sentences) - 1:
                    sentence += '.'
                
                self.tts_engine.say(sentence.strip())
                self.tts_engine.runAndWait()
                
                # Small pause between sentences for natural flow
                if i < len(sentences) - 1:
                    time.sleep(0.2)

    def listen_for_audio(self):
        """Listen for audio input and add to queue"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Error in audio listening: {e}")
                continue

    def speech_to_text(self, audio) -> Optional[str]:
        """Convert speech to text"""
        try:
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            return None

    def get_ollama_response(self, user_input: str) -> str:
        """Get response from Ollama model as ARKA"""
        try:
            # Add context about being ARKA - a friendly 25-year-old Indian guy
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
            
            # Prepare conversation context
            messages = [{'role': 'system', 'content': system_prompt}]
            
            # Add conversation history (last 8 exchanges for more natural context)
            for msg in self.conversation_history[-16:]:
                messages.append(msg)
            
            # Add current user input
            messages.append({'role': 'user', 'content': user_input})
            
            # Get response from Ollama
            response = ollama.chat(model=self.model_name, messages=messages)
            
            bot_response = response['message']['content']
            
            # Post-process response to add ARKA's personality
            bot_response = self._make_speech_natural_indian(bot_response)
            
            # Update conversation history
            self.conversation_history.append({'role': 'user', 'content': user_input})
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            return bot_response
            
        except Exception as e:
            error_msg = f"Yaar, I'm having some technical issues right now. Can you try asking that again?"
            print(f"Ollama error: {e}")
            return error_msg

    def _make_speech_natural_indian(self, text: str) -> str:
        """Post-process text to add Indian English patterns and natural speech"""
        import re
        
        # Add natural pauses with commas for Indian English rhythm
        text = re.sub(r'(\w+)\s+(actually|basically|obviously|totally|yaar|definitely)\s+', r'\1, \2, ', text)
        
        # Make sure contractions are used
        contractions = {
            'I am': "I'm", 'you are': "you're", 'it is': "it's", 'that is': "that's",
            'I will': "I'll", 'you will': "you'll", 'I would': "I'd", 'you would': "you'd",
            'cannot': "can't", 'do not': "don't", 'does not': "doesn't", 'will not': "won't",
            'should not': "shouldn't", 'could not': "couldn't", 'would not': "wouldn't"
        }
        
        for full, contraction in contractions.items():
            text = re.sub(r'\b' + full + r'\b', contraction, text, flags=re.IGNORECASE)
        
        # Add slight pauses for more natural Indian English flow
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Occasionally add Indian English expressions if not already present
        if len(text) > 50 and not any(word in text.lower() for word in ['yaar', 'actually', 'basically', 'totally']):
            if 'great' in text.lower():
                text = text.replace('great', 'totally great')
            elif 'good' in text.lower():
                text = text.replace('good', 'really good')
        
        return text.strip()

    def process_command(self, text: str) -> bool:
        """Process special commands, return True if command was processed"""
        text_lower = text.lower().strip()
        
        if any(word in text_lower for word in ['exit', 'quit', 'goodbye', 'stop', 'end']):
            self.speak("Arre yaar, it was totally awesome chatting with you! Take care, and definitely come back soon, okay? Bye!")
            return True
        elif 'clear history' in text_lower or 'reset conversation' in text_lower:
            self.conversation_history.clear()
            self.speak("Perfect! I've cleared our conversation history, yaar. We're starting fresh now! So, what would you like to talk about?")
            return False
        elif 'help' in text_lower and len(text_lower.split()) == 1:
            help_text = """Hey! I'm ARKA, and I'm here to chat about basically anything you'd like, yaar! You can ask me questions, get help with tasks, or just have a friendly conversation. If you want to start fresh, just say 'clear history', and if you need to go, say 'exit' or 'goodbye'. What would you like to talk about today?"""
            self.speak(help_text)
            return False
        
        return False

    def run(self):
        """Main loop for the voice bot"""
        self.speak("Hey there! I'm ARKA, your friendly voice assistant! I'm really excited to chat with you today, yaar! What can I help you with?")
        
        self.is_listening = True
        
        # Start audio listening thread
        audio_thread = threading.Thread(target=self.listen_for_audio, daemon=True)
        audio_thread.start()
        
        try:
            while True:
                # Check for audio in queue
                try:
                    audio = self.audio_queue.get(timeout=0.1)
                    
                    print("Processing speech...")
                    text = self.speech_to_text(audio)
                    
                    if text:
                        print(f"You said: {text}")
                        
                        # Process special commands
                        if self.process_command(text):
                            break
                        
                        # Get AI response
                        print("Thinking...")
                        response = self.get_ollama_response(text)
                        
                        # Speak the response
                        self.speak(response)
                    else:
                        print("Could not understand audio, please try again.")
                        
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    print("\nShutting down...")
                    break
                    
        finally:
            self.is_listening = False
            self.speak("Thanks for chatting with me today, yaar! Have a totally awesome day ahead!")

def main():
    """Main function to run ARKA - the Indian voice bot"""
    print("=== ARKA - Your Indian Voice Assistant ===")
    print("A friendly 25-year-old Indian guy ready to chat!")
    print("Make sure Ollama is installed and running!")
    print("Press Ctrl+C to exit\n")
    
    try:
        # Initialize and run ARKA
        bot = VoiceToVoiceBot(model_name="gemma3:latest")
        bot.run()
        
    except KeyboardInterrupt:
        print("\nGoodbye from ARKA!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()