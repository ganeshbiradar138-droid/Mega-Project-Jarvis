# Mega Project Jarvis

A Python voice assistant that listens for the wake word **Jarvis**, recognizes spoken commands, opens websites, fetches top news headlines, and can answer general questions using a local Ollama model.

## Features

- Voice input with SpeechRecognition
- Text-to-speech responses with pyttsx3
- Open common websites using voice commands
- Fetch top headlines using NewsAPI
- Optional local AI chat using Ollama and `llama3.2:3b`

## Requirements

- Python 3.10 or newer
- A working microphone
- Internet connection for speech recognition and NewsAPI
- Ollama installed and running for the optional AI chat feature

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/ganeshbiradar138-droid/Mega-Project-Jarvis.git
   cd Mega-Project-Jarvis
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your own NewsAPI key. Set the `NEWS_API_KEY` environment variable in your terminal or load `.env` with your preferred environment-variable loader.
5. For AI chat, install Ollama, start it, and pull the model:
   ```bash
   ollama pull llama3.2:3b
   ```
6. Run the main assistant:
   ```bash
   python jarvis.py
   ```

## Voice commands

- Say **Jarvis** to activate the assistant.
- Say **open YouTube**, **open Google**, **open GitHub**, etc.
- Say **news** to hear the latest headlines.
- Ask a general question to use the local Ollama model.
- Say **stop** to end the active command session.
- Press **Ctrl+C** to exit.

## Security

Never commit your real API keys or `.env` file. Keep credentials in environment variables. The repository intentionally excludes virtual environments, Python cache files, and local secrets.

## Project files

- `jarvis.py` – current assistant with optional Ollama chat
- `main.py` – earlier command-based assistant version
- `requirements.txt` – Python dependencies
- `.env.example` – environment-variable template
