#!/bin/bash

# Voice-to-Voice Bot Setup Script
# This script installs all dependencies and sets up the bot

echo "=== Voice-to-Voice Bot Setup ==="
echo "Setting up your offline voice bot with Ollama Gemma 3..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3."
    exit 1
fi

# Install system dependencies for audio (macOS)
echo "Installing system dependencies..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        echo "Installing PortAudio via Homebrew..."
        brew install portaudio
    else
        echo "Homebrew not found. Please install PortAudio manually:"
        echo "Visit: https://www.portaudio.com/"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Installing PortAudio via apt..."
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Installing Ollama..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Please download and install Ollama from: https://ollama.ai/"
        echo "Or run: brew install ollama"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    echo "After installing Ollama, please run: ollama serve"
    echo "Then run this setup script again."
    exit 1
fi

# Start Ollama service
echo "Starting Ollama service..."
ollama serve &
sleep 3

# Pull Gemma 2 model (Gemma 3)
echo "Downloading Gemma 2 model (this may take a while)..."
ollama pull gemma2

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run the voice bot:"
echo "  python3 voice2voice.py"
echo ""
echo "To run the enhanced bot with text/voice modes:"
echo "  cd ollama-bot/src && python3 main.py"
echo ""
echo "Make sure Ollama is running before starting the bot!"
echo "If Ollama is not running, start it with: ollama serve"
