# Voice-to-Voice Bot with Ollama Gemma 3

An offline voice assistant that can speak with users, understand their requirements, and provide intelligent responses using the Ollama Gemma 3 (gemma2) model.

## Features

- 🎤 **Voice Input**: Real-time speech recognition
- 🔊 **Voice Output**: Natural text-to-speech responses  
- 🧠 **AI Intelligence**: Powered by Ollama Gemma 3 model
- 💬 **Conversation Memory**: Maintains context across conversations
- 🔄 **Dual Modes**: Both voice-only and text+voice interaction
- 🏠 **Fully Offline**: No internet required after setup

## Quick Start

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai/)
3. **System audio libraries** (automatically installed by setup script)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/arkabera/Desktop/SMITBOT
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start Ollama service** (if not already running):
   ```bash
   ollama serve
   ```

### Usage

#### Option 1: Pure Voice Bot
```bash
python3 voice2voice.py
```
- Fully voice-controlled interface
- Speak naturally to interact
- Say "exit" or "goodbye" to quit

#### Option 2: Enhanced Bot (Text + Voice)
```bash
cd ollama-bot/src
python3 main.py
```
- Start with text input
- Type `voice` to switch to voice mode
- Type `exit` to quit

## Manual Installation

If the setup script doesn't work, install manually:

### 1. Install System Dependencies

**macOS:**
```bash
brew install portaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Install and Setup Ollama

**macOS:**
```bash
brew install ollama
# or download from https://ollama.ai/
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Start Ollama:**
```bash
ollama serve
```

**Download Gemma 3 model:**
```bash
ollama pull gemma2
```

## Voice Commands

- **"Exit"** / **"Goodbye"** / **"Quit"** - End conversation
- **"Clear history"** / **"Reset conversation"** - Clear conversation memory
- **"Help"** - Get help information
- **"Exit voice mode"** - Return to text mode (in enhanced bot)

## Troubleshooting

### Common Issues

1. **Microphone not working:**
   - Check microphone permissions in System Preferences (macOS)
   - Ensure microphone is not muted
   - Try adjusting microphone sensitivity

2. **PyAudio installation fails:**
   ```bash
   # macOS
   brew install portaudio
   pip3 install pyaudio
   
   # Linux
   sudo apt-get install portaudio19-dev
   pip3 install pyaudio
   ```

3. **Ollama connection error:**
   - Ensure Ollama is running: `ollama serve`
   - Check if model is downloaded: `ollama list`
   - Download model manually: `ollama pull gemma2`

4. **Speech recognition not working:**
   - Check internet connection (Google Speech API requires internet)
   - Speak clearly and closer to microphone
   - Reduce background noise

### Performance Tips

- **Model Performance**: Gemma 2 works best with at least 8GB RAM
- **Audio Quality**: Use a good quality microphone for better recognition
- **Response Time**: First response may be slower as the model loads

## Configuration

### Changing Models
Edit the model name in the code:
```python
# In voice2voice.py or ollama_client.py
bot = VoiceToVoiceBot(model_name="gemma2")  # or "llama2", "mistral", etc.
```

### Voice Settings
Modify TTS settings in `voice2voice.py`:
```python
self.tts_engine.setProperty('rate', 180)    # Speech speed
self.tts_engine.setProperty('volume', 0.9)  # Volume level
```

## Project Structure

```
SMITBOT/
├── voice2voice.py          # Main voice bot application
├── requirements.txt        # Python dependencies
├── setup.sh               # Installation script
├── README.md              # This file
└── ollama-bot/            # Enhanced bot with text/voice modes
    ├── requirements.txt
    └── src/
        ├── main.py        # Enhanced bot entry point
        └── bot/
            ├── ollama_client.py    # Ollama API client
            └── conversation.py     # Conversation handler
```

## Available Models

You can use different Ollama models by changing the model name:
- `gemma2` (Gemma 3) - Recommended
- `llama2` - Good general purpose
- `mistral` - Fast and efficient
- `codellama` - Good for coding questions

## Contributing

Feel free to contribute improvements:
1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify Ollama is running and model is downloaded
4. Check system microphone permissions
