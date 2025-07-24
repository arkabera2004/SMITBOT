# 🇮🇳 ARKA - Your Indian Voice Assistant

## 👨‍💻 Meet ARKA

**ARKA** is your friendly 25-year-old Indian voice assistant with a natural, enthusiastic personality! He's designed to sound like a real Indian friend who's always excited to help and chat.

### ✅ ARKA's Personality:

- **Age**: 25 years old
- **Gender**: Male
- **Accent**: Indian English with natural expressions
- **Personality**: Enthusiastic, friendly, helpful, and genuinely excited to chat
- **Voice**: Uses "Daniel" voice (best available male voice) with optimized settings

### 🎤 Voice Characteristics:

- **Speed**: 155 WPM (energetic but clear)
- **Volume**: 0.85 (confident and clear)
- **Pitch**: Slightly lower (-0.1) for masculine sound
- **Inflection**: Enhanced (0.15) for expressive Indian English

### 💬 Speech Patterns:

ARKA uses natural Indian English expressions:
- **Indian expressions**: "yaar", "actually", "basically", "totally", "obviously"
- **Enthusiasm**: "That's awesome!", "Cool!", "Amazing!", "Interesting!"
- **Natural contractions**: "I'm", "you're", "don't", "can't"
- **Indian English patterns**: "I am telling you", "What to do", "Like that only"

### 🗣️ Example Conversations:

**Greeting**: 
> "Hey there! I'm ARKA, your friendly voice assistant! I'm really excited to chat with you today, yaar! What can I help you with?"

**Helping**: 
> "That's totally awesome! I'd love to help you with that. Actually, I think I have some great ideas for you!"

**Goodbye**: 
> "Arre yaar, it was totally awesome chatting with you! Take care, and definitely come back soon, okay? Bye!"

### 🚀 How to Chat with ARKA:

#### Option 1: Pure Voice Mode
```bash
python3 voice2voice.py
```
- Direct voice-to-voice conversation with ARKA
- Most natural experience

#### Option 2: Enhanced Mode
```bash
cd ollama-bot/src && python3 main.py
```
- Text and voice options
- Type "voice" to switch to voice mode

#### Option 3: Easy Launcher
```bash
python3 run_bot.py
```
- Choose your preferred mode
- Includes voice testing option

### 🎯 Voice Commands for ARKA:

- **"Hey ARKA"** - Get his attention
- **"Help"** - Get assistance options
- **"Clear history"** - Reset conversation
- **"Exit voice mode"** - Switch to text (enhanced mode)
- **"Goodbye"** / **"Exit"** - End conversation

### 🔧 Configuration:

ARKA's settings are stored in `.env`:
```properties
BOT_NAME=ARKA
BOT_AGE=25
BOT_ACCENT=indian
TTS_RATE=155
TTS_VOLUME=0.85
PREFERRED_VOICE=indian_male
```

### 🎪 Test ARKA's Voice:

```bash
python3 test_arka.py
```

This will let you hear ARKA's natural Indian English speech patterns and enthusiastic personality!

### 🌟 What Makes ARKA Special:

1. **Authentic Indian Personality**: Sounds like a real 25-year-old Indian friend
2. **Natural Speech Patterns**: Uses genuine Indian English expressions
3. **Enthusiastic & Helpful**: Always excited to assist and chat
4. **Male Voice**: Optimized male voice with natural pitch
5. **Cultural Authenticity**: Uses "yaar" and other Indian expressions naturally
6. **Smart Conversations**: Powered by Gemma 3 with Indian context

---

**Ready to chat with ARKA? He's waiting to meet you, yaar!** 🎉
