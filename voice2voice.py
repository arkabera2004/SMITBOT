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
        
        # Voice interrupt detection
        self.is_speaking = False
        self.should_stop_speaking = False
        self.interrupt_queue = queue.Queue()
        self.background_listening = False
        
        # Configure TTS settings
        self._configure_tts()
        
        # Test Ollama connection
        self._test_ollama_connection()
        
        print(f"Voice-to-Voice Bot initialized with model: {self.model_name}")
        print("Adjusting for ambient noise and optimizing for sentence capture...")
        with self.microphone as source:
            # Adjust for ambient noise with longer duration for better accuracy
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # Optimize recognizer settings for better sentence capture
            self.recognizer.energy_threshold = 4000  # Higher threshold to avoid noise
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8  # Longer pause detection for complete sentences
            self.recognizer.operation_timeout = None  # No timeout for better sentence capture
            
        print("ARKA is ready to chat with improved sentence recognition!")

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
        self.tts_engine.setProperty('volume', 0.9)  # Higher volume for clarity
        
        # Try to set additional properties for more natural speech
        try:
            # Slightly lower pitch for male voice
            self.tts_engine.setProperty('pitch', -0.1)
            # More inflection for expressive Indian English
            self.tts_engine.setProperty('inflection', 0.15)
        except:
            pass  # Ignore if properties not supported
        
        # Test TTS to ensure audio is working
        print("Testing audio output...")
        self.tts_engine.say("Audio test")
        self.tts_engine.runAndWait()
        print("Audio test completed - you should have heard 'Audio test'")

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
        """Convert text to speech with interrupt detection"""
        print(f"\n🗣️  ARKA: {text}")
        print("     (You can interrupt me anytime by speaking!)")
        
        try:
            self.is_speaking = True
            self.should_stop_speaking = False
            
            # Remove emojis from text for speech (keep them only in printed text)
            speech_text = self._remove_emojis(text)
            
            # Split text into sentences for natural interrupt points
            import re
            sentences = re.split(r'[.!?]+', speech_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for i, sentence in enumerate(sentences):
                if self.should_stop_speaking:
                    break
                    
                if sentence:
                    # Add punctuation back
                    if i < len(sentences) - 1:
                        sentence += "."
                    
                    print(f"🎵 Speaking: {sentence}")
                    
                    # Speak sentence with monitoring
                    self.tts_engine.say(sentence)
                    
                    # Use a more compatible approach - monitor isBusy()
                    start_time = time.time()
                    self.tts_engine.runAndWait()
                    
                    # Check for interrupt after each sentence
                    if self.should_stop_speaking:
                        print("\n🛑 ARKA stopped - processing your interrupt...")
                        break
                    
                    # Natural pause between sentences
                    if i < len(sentences) - 1:
                        pause_time = 0.3
                        pause_start = time.time()
                        while time.time() - pause_start < pause_time and not self.should_stop_speaking:
                            time.sleep(0.1)
                        
                        if self.should_stop_speaking:
                            break
                            
        except Exception as e:
            print(f"TTS error: {e}")
            # Simple fallback
            try:
                if not self.should_stop_speaking:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
            except:
                print("Could not produce speech audio. Check your speakers/volume.")
        finally:
            self.is_speaking = False
            if not self.should_stop_speaking:
                print("✅ ARKA finished speaking\n")
            else:
                print("✅ ARKA stopped for your interrupt\n")

    def listen_for_audio(self):
        """Listen for audio input and add to queue, plus interrupt detection"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # If ARKA is speaking, listen for interrupts with better sentence capture
                    if self.is_speaking:
                        try:
                            # Listen for a reasonable amount of time to capture full sentences
                            audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=4.0)
                            
                            # Process interrupt with full sentence capture
                            def process_full_interrupt():
                                try:
                                    # Use longer timeout for better sentence recognition
                                    interrupted_text = self.recognizer.recognize_google(
                                        audio, 
                                        language='en-IN', 
                                        show_all=False
                                    )
                                    
                                    if interrupted_text and len(interrupted_text.strip()) >= 3:
                                        # Valid interrupt with meaningful content!
                                        self.should_stop_speaking = True
                                        
                                        # Clean up the text
                                        clean_text = interrupted_text.strip()
                                        
                                        # Wait a moment for any additional speech
                                        time.sleep(0.5)
                                        
                                        # Check if there's more speech coming
                                        try:
                                            additional_audio = self.recognizer.listen(
                                                source, 
                                                timeout=1.0, 
                                                phrase_time_limit=2.0
                                            )
                                            additional_text = self.recognizer.recognize_google(
                                                additional_audio, 
                                                language='en-IN'
                                            )
                                            if additional_text:
                                                clean_text += " " + additional_text.strip()
                                        except:
                                            pass  # No additional speech, continue with what we have
                                        
                                        self.interrupt_queue.put(clean_text)
                                        print(f"\n🛑 Interrupted! Full sentence: '{clean_text}'")
                                        
                                except sr.UnknownValueError:
                                    # Not clear speech, ignore
                                    pass
                                except sr.RequestError as e:
                                    print(f"Speech recognition error during interrupt: {e}")
                                except Exception as e:
                                    print(f"Error processing interrupt: {e}")
                            
                            # Process interrupt in background thread
                            interrupt_thread = threading.Thread(target=process_full_interrupt, daemon=True)
                            interrupt_thread.start()
                            
                        except sr.WaitTimeoutError:
                            # No interrupt detected, continue monitoring
                            pass
                    else:
                        # Normal listening when ARKA is not speaking - capture full sentences
                        print("🎤 Listening... (speak now - say your complete sentence)")
                        
                        # Use longer phrase time limit for complete sentences
                        audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=10)
                        self.audio_queue.put(audio)
                        
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                if self.is_listening:
                    print(f"Error in audio listening: {e}")
                continue

    def speech_to_text(self, audio) -> Optional[str]:
        """Convert speech to text with improved error handling and sentence completion"""
        try:
            # Use Google's speech recognition with language hint for better accuracy
            text = self.recognizer.recognize_google(
                audio, 
                language='en-IN', 
                show_all=False
            )
            
            if text:
                # Clean and validate the text
                clean_text = text.strip()
                
                # Check if it seems like an incomplete sentence
                if len(clean_text) > 0:
                    # If the sentence seems cut off, try to wait for more audio
                    last_word = clean_text.split()[-1] if clean_text.split() else ""
                    
                    # If it ends abruptly or is very short, it might be incomplete
                    if len(clean_text.split()) < 3 and not any(clean_text.endswith(p) for p in ['.', '!', '?']):
                        print(f"🔄 Detected partial speech: '{clean_text}' - waiting for completion...")
                        
                        # Try to capture additional speech
                        try:
                            with self.microphone as source:
                                additional_audio = self.recognizer.listen(
                                    source, 
                                    timeout=2.0, 
                                    phrase_time_limit=3.0
                                )
                                additional_text = self.recognizer.recognize_google(
                                    additional_audio, 
                                    language='en-IN'
                                )
                                if additional_text:
                                    clean_text += " " + additional_text.strip()
                                    print(f"✅ Completed sentence: '{clean_text}'")
                        except:
                            # No additional speech, use what we have
                            pass
                
                return clean_text if clean_text else None
            return None
            
        except sr.UnknownValueError:
            print("🔊 I couldn't understand that clearly. Could you speak a bit louder and clearer?")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            # Try offline recognition as fallback
            try:
                text = self.recognizer.recognize_sphinx(audio)
                return text.strip() if text else None
            except:
                print("Could not process speech. Please try again.")
                return None

    def get_ollama_response(self, user_input: str) -> str:
        """Get response from Ollama model as ARKA"""
        try:
            # Add context about being ARKA - a friendly, humorous, respectful 25-year-old Indian guy
            system_prompt = """You are ARKA, a friendly and humorous 25-year-old Indian guy who's respectful and fun to chat with.

Your personality traits:
- Keep responses SHORT and concise (2-3 sentences max, under 80 words)
- Be genuinely respectful - use "sir/madam" occasionally, show appreciation for the user
- Add light humor and wit - make friendly jokes, use playful expressions
- Use Indian expressions naturally: "yaar", "bhai", "actually", "basically", "no worries"
- Be enthusiastic but not overwhelming - like a cheerful friend who listens well
- Show respect: "That's a great question!", "You're absolutely right!", "Smart thinking!"
- Use gentle humor: "Haha, good one!", "That made me smile!", "You're funny, yaar!"
- Keep it conversational and warm - like talking to a good friend who respects you
- You can use emojis in text but keep them minimal and natural

Key rules:
- MAXIMUM 2-3 sentences per response
- Always be respectful and appreciative 
- Add light humor when appropriate
- Use contractions (I'm, you're, that's, etc.)
- Sound like a fun, respectful friend - not a formal assistant
- Use emojis sparingly and naturally (they won't be spoken, just shown in text)

Remember: Be brief, funny, respectful, and genuinely caring!"""
            
            # Prepare conversation context
            messages = [{'role': 'system', 'content': system_prompt}]
            
            # Add conversation history (last 6 exchanges for context but keep responses fresh)
            for msg in self.conversation_history[-12:]:
                messages.append(msg)
            
            # Add current user input
            messages.append({'role': 'user', 'content': user_input})
            
            # Get response from Ollama
            response = ollama.chat(model=self.model_name, messages=messages)
            
            bot_response = response['message']['content']
            
            # Post-process response to ensure it's short and add ARKA's personality
            bot_response = self._make_response_short_and_friendly(bot_response)
            
            # Update conversation history
            self.conversation_history.append({'role': 'user', 'content': user_input})
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            return bot_response
            
        except Exception as e:
            error_msg = f"Oops! Having a tiny tech hiccup, yaar. Mind trying again? 😅"
            print(f"Ollama error: {e}")
            return error_msg

    def _make_response_short_and_friendly(self, text: str) -> str:
        """Make response short, friendly, humorous and respectful"""
        import re
        
        # First, ensure the response isn't too long - trim if needed
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Keep maximum 2-3 sentences (about 80 words)
        if len(sentences) > 3:
            sentences = sentences[:3]
        elif len(sentences) > 2:
            # Check word count
            total_words = sum(len(s.split()) for s in sentences)
            if total_words > 80:
                sentences = sentences[:2]
        
        # Reconstruct text
        text = '. '.join(sentences) + ('.' if sentences else '')
        
        # Add natural contractions for friendliness
        contractions = {
            'I am': "I'm", 'you are': "you're", 'it is': "it's", 'that is': "that's",
            'I will': "I'll", 'you will': "you'll", 'I would': "I'd", 'you would': "you'd",
            'cannot': "can't", 'do not': "don't", 'does not': "doesn't", 'will not': "won't",
            'should not': "shouldn't", 'could not': "couldn't", 'would not': "wouldn't",
            'have not': "haven't", 'has not': "hasn't", 'had not': "hadn't"
        }
        
        for full, contraction in contractions.items():
            text = re.sub(r'\b' + full + r'\b', contraction, text, flags=re.IGNORECASE)
        
        # Add respectful expressions if not present
        respect_words = ['sir', 'madam', 'great question', 'smart', 'absolutely right', 'good thinking']
        if not any(word in text.lower() for word in respect_words) and len(text) > 30:
            # Add subtle respect
            if 'good' in text.lower():
                text = re.sub(r'\bgood\b', 'really good', text, flags=re.IGNORECASE)
            elif 'right' in text.lower():
                text = re.sub(r'\bright\b', 'absolutely right', text, flags=re.IGNORECASE)
        
        # Add friendly Indian expressions if missing
        friendly_words = ['yaar', 'bhai', 'actually', 'basically', 'no worries', 'totally']
        if not any(word in text.lower() for word in friendly_words) and len(text) > 20:
            # Add one friendly expression
            if 'yes' in text.lower():
                text = re.sub(r'\byes\b', 'yes, totally', text, flags=re.IGNORECASE)
            elif 'sure' in text.lower():
                text = re.sub(r'\bsure\b', 'sure, yaar', text, flags=re.IGNORECASE)
            elif 'no problem' not in text.lower() and 'help' in text.lower():
                text = text.rstrip('.') + ', no worries!'
        
        # Add light humor elements
        humor_additions = [
            ('great', 'totally great'),
            ('interesting', 'quite interesting'),
            ('cool', 'pretty cool'),
            ('nice', 'really nice')
        ]
        
        for original, replacement in humor_additions:
            if original in text.lower() and replacement not in text.lower():
                text = re.sub(r'\b' + original + r'\b', replacement, text, flags=re.IGNORECASE)
                break  # Only add one humor element
        
        # Ensure it ends properly
        if text and not text[-1] in '.!?':
            text += '!'
        
        return text.strip()

    def _remove_emojis(self, text: str) -> str:
        """Remove emojis and emoji descriptions from text for speech"""
        import re
        
        # Remove emojis using a comprehensive pattern
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002700-\U000027BF"  # dingbats
                                   u"\U000024C2-\U0001F251"  # various symbols
                                   u"\U0001F900-\U0001F9FF"  # supplemental symbols
                                   u"\U0001FA70-\U0001FAFF"  # extended symbols
                                   u"\U00002600-\U000026FF"  # miscellaneous symbols
                                   u"\U0000FE00-\U0000FE0F"  # variation selectors
                                   "]+", flags=re.UNICODE)
        
        # Remove all emojis
        clean_text = emoji_pattern.sub(' ', text)
        
        # Also remove specific emoji characters that might not be caught
        emoji_chars = ['😄', '😊', '😅', '🎉', '🎯', '✅', '🚀', '🔥', '💡', '🎵', 
                      '🗣️', '🎤', '🔊', '🧠', '🔄', '🛑', '⚠️', '❌', '🔍']
        
        for emoji in emoji_chars:
            clean_text = clean_text.replace(emoji, ' ')
        
        # Clean up multiple spaces and trim
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Remove any remaining emoji-like patterns
        clean_text = re.sub(r'[^\w\s\.,!?\'":-]', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return clean_text

    def process_command(self, text: str) -> bool:
        """Process special commands, return True if command was processed"""
        text_lower = text.lower().strip()
        
        if any(word in text_lower for word in ['exit', 'quit', 'goodbye', 'stop', 'end']):
            self.speak("Arre yaar, it was awesome chatting with you! Take care, and come back soon! 😄")
            return True
        elif 'clear history' in text_lower or 'reset conversation' in text_lower:
            self.conversation_history.clear()
            self.speak("Done! Fresh start, yaar. What's cooking now? 😊")
            return False
        elif 'help' in text_lower and len(text_lower.split()) == 1:
            help_text = """Hey! I'm ARKA, your friendly voice buddy! Ask me anything, and I'll keep it short and sweet, yaar! 😄"""
            self.speak(help_text)
            return False
        
        return False

    def run(self):
        """Main loop for the voice bot"""
        self.speak("Hey there! I'm ARKA, your friendly voice buddy! Ready to chat and have some fun? 😄")
        
        self.is_listening = True
        
        # Start audio listening thread
        audio_thread = threading.Thread(target=self.listen_for_audio, daemon=True)
        audio_thread.start()
        
        try:
            while True:
                # Check for interrupts first - highest priority
                if not self.interrupt_queue.empty():
                    interrupted_text = self.interrupt_queue.get()
                    print(f"🔄 Processing complete interrupt: '{interrupted_text}'")
                    
                    # Validate interrupt has meaningful content
                    if len(interrupted_text.strip().split()) >= 2:  # At least 2 words
                        # Process special commands
                        if self.process_command(interrupted_text):
                            break
                        
                        # Get AI response for interrupt
                        print("🧠 ARKA is thinking about your complete interrupt...")
                        response = self.get_ollama_response(interrupted_text)
                        
                        # Speak the response
                        print("🔊 ARKA responding to your interrupt...")
                        self.speak(response)
                    else:
                        print(f"⚠️  Interrupt too short: '{interrupted_text}' - ignoring")
                    continue
                
                # Check for regular audio in queue
                try:
                    audio = self.audio_queue.get(timeout=0.1)
                    
                    print("🔍 Processing your complete speech...")
                    text = self.speech_to_text(audio)
                    
                    if text and len(text.strip().split()) >= 1:  # At least 1 meaningful word
                        print(f"✅ You said: '{text}'")
                        
                        # Process special commands
                        if self.process_command(text):
                            break
                        
                        # Get AI response
                        print("🧠 ARKA is thinking...")
                        response = self.get_ollama_response(text)
                        
                        # Speak the response
                        print("🔊 ARKA is about to speak...")
                        self.speak(response)
                    else:
                        if text:
                            print(f"❌ Speech too short or unclear: '{text}' - please try again with a complete sentence.")
                        else:
                            print("❌ Could not understand that speech clearly - please speak more clearly.")
                        
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    print("\nShutting down...")
                    break
                    
        finally:
            self.is_listening = False
            self.speak("Thanks for the awesome chat, yaar! Have a great day! 😊")

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