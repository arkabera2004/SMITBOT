import speech_recognition as sr
import pyttsx3
import time
from typing import Optional

class Conversation:
    def __init__(self, ollama_client):
        """
        Initialize conversation handler
        
        Args:
            ollama_client: Instance of OllamaClient
        """
        self.ollama_client = ollama_client
        
        # Initialize speech recognition and TTS (optional for voice mode)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS
        self._configure_tts()

    def _configure_tts(self):
        """Configure Text-to-Speech settings for natural voice"""
        try:
            voices = self.tts_engine.getProperty('voices')
            
            # Try to find the most natural sounding voice
            best_voice = None
            preferred_voices = [
                'samantha', 'alex', 'victoria', 'allison', 'ava', 'susan', 'karen',
                'tessa', 'veena', 'fiona', 'moira', 'nicky', 'emily', 'kate'
            ]
            
            if voices:
                # First try to find preferred natural voices
                for voice in voices:
                    voice_name = voice.name.lower()
                    for preferred in preferred_voices:
                        if preferred in voice_name:
                            best_voice = voice
                            break
                    if best_voice:
                        break
                
                # If no preferred voice found, try to find any female voice
                if not best_voice:
                    for voice in voices:
                        if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'samantha', 'alex']):
                            best_voice = voice
                            break
                
                # Use the best voice found
                if best_voice:
                    self.tts_engine.setProperty('voice', best_voice.id)
                elif voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set natural speech parameters
            self.tts_engine.setProperty('rate', 160)    # Slower, more natural speed
            self.tts_engine.setProperty('volume', 0.8)  # Slightly softer volume
            
        except Exception as e:
            print(f"TTS configuration warning: {e}")

    def start(self):
        """Start text-based conversation (compatible with original method name)"""
        self.start_conversation()

    def start_conversation(self):
        """Start text-based conversation loop"""
        print("Welcome! I'm ARKA, your friendly Indian voice assistant! How can I help you today, yaar?")
        print("Type 'voice' to switch to voice mode, 'exit' or 'quit' to end.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'goodbye']:
                    print("ARKA: Arre yaar, it was totally awesome chatting with you! Take care!")
                    break
                elif user_input.lower() == 'voice':
                    result = self.start_voice_conversation()
                    if result == "exit":
                        break
                    continue
                elif user_input.lower() == 'clear':
                    self.ollama_client.clear_history()
                    continue
                elif not user_input:
                    continue
                
                response = self.process_input(user_input)
                print(f"\nARKA: {response}")
                
            except KeyboardInterrupt:
                print("\nARKA: Thanks for chatting with me, yaar! Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def start_voice_conversation(self):
        """Start voice-based conversation"""
        print("\n=== ARKA Voice Mode Activated ===")
        print("Speak clearly. Say 'exit voice mode' to return to text mode.")
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.speak("Hey! ARKA's voice mode is active now, yaar! I'm listening!")
        except Exception as e:
            print(f"Microphone setup error: {e}")
            print("Returning to text mode...")
            return
        
        while True:
            try:
                print("\nListening...")
                
                # Listen for audio
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                # Convert speech to text
                print("Processing speech...")
                text = self.speech_to_text(audio)
                
                if text:
                    print(f"You said: {text}")
                    
                    # Check for exit commands
                    if any(phrase in text.lower() for phrase in ['exit voice mode', 'text mode', 'stop voice']):
                        self.speak("Cool, switching back to text mode, yaar!")
                        break
                    elif any(phrase in text.lower() for phrase in ['exit', 'quit', 'goodbye']):
                        self.speak("Arre yaar, it was awesome chatting! Take care!")
                        return "exit"
                    
                    # Get and speak response
                    response = self.process_input(text)
                    print(f"\nARKA: {response}")
                    self.speak(response)
                else:
                    print("Could not understand. Please try again.")
                    
            except sr.WaitTimeoutError:
                print("No speech detected. Say something or 'exit voice mode'...")
            except KeyboardInterrupt:
                print("\nExiting voice mode...")
                break
            except Exception as e:
                print(f"Voice error: {e}")
                
        print("=== Returned to Text Mode ===")
        return None

    def speech_to_text(self, audio) -> Optional[str]:
        """Convert speech to text"""
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

    def speak(self, text: str):
        """Convert text to speech with natural pauses"""
        try:
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
        except Exception as e:
            print(f"TTS error: {e}")

    def process_input(self, user_input: str) -> str:
        """
        Process user input and get response from Ollama
        
        Args:
            user_input: User's input text
            
        Returns:
            Bot response string
        """
        try:
            response = self.ollama_client.get_response(user_input)
            return response
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"