# Ollama Bot

## Overview
Ollama Bot is an offline conversational agent that utilizes the Ollama model Gemma3 to interact with users. The bot is designed to understand user requirements and respond to queries effectively.

## Project Structure
```
ollama-bot/
├── src/
│   ├── main.py               # Entry point of the application
│   ├── bot/
│   │   ├── __init__.py       # Bot package initialization
│   │   ├── ollama_client.py   # Handles interactions with the Ollama model
│   │   └── conversation.py     # Manages dialogue flow with the user
│   ├── config/
│   │   ├── __init__.py       # Config package initialization
│   │   └── settings.py       # Configuration settings for the bot
│   └── utils/
│       ├── __init__.py       # Utils package initialization
│       └── helpers.py        # Utility functions for the bot
├── requirements.txt           # Project dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files to ignore in version control
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ollama-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the necessary values.

## Usage
To run the bot, execute the following command:
```
python src/main.py
```

## Features
- Interactive conversation with users.
- Utilizes the Ollama model Gemma3 for generating responses.
- Configurable settings for model parameters and API keys.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.