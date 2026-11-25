# J.A.R.V.I.S — Personal AI Desktop Assistant

A Python-based desktop voice assistant with a modern Tkinter interface. Jarvis can respond to typed questions, listen to voice commands, open frequently used websites, fetch top Indian news headlines, and use a local Ollama model for AI chat.

> **Current interface:** Desktop GUI built with Python Tkinter. This is a local desktop application, not a hosted website.

## Preview of features

- Dark dashboard-style interface with conversation history
- Text chat input and voice-command button
- Quick actions for Google, YouTube, GitHub, music, news, and help
- Text-to-speech responses
- Optional local AI chat using Ollama and `llama3.2:3b`
- News headlines through NewsAPI

## Project structure

```
Mega-Project-Jarvis/
├── ui.py                 # Tkinter desktop user interface
├── jarvis.py             # Assistant logic, AI, speech, news, commands
├── main.py               # Earlier command-line version
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore
└── README.md
```

## Requirements

- Windows, macOS, or Linux with Python 3.10+
- Microphone for voice commands
- Internet connection for speech recognition and NewsAPI
- Ollama installed and running for local AI chat (optional)

Tkinter is included with most standard Python installations. On some Linux distributions, install the system package `python3-tk`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ganeshbiradar138-droid/Mega-Project-Jarvis.git
   cd Mega-Project-Jarvis
   ```

2. Create and activate a virtual environment:

   **Windows**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure NewsAPI (optional). Copy `.env.example` to `.env`, add your own key, and set `NEWS_API_KEY` in your environment before launching. The application reads environment variables; it does not automatically load the `.env` file.

   **PowerShell (current terminal only):**
   ```powershell
   $env:NEWS_API_KEY="your_newsapi_key"
   ```

   **macOS / Linux (current terminal only):**
   ```bash
   export NEWS_API_KEY="your_newsapi_key"
   ```

5. For AI chat, install Ollama, start the Ollama service, and download the model:

   ```bash
   ollama pull llama3.2:3b
   ```

## Run the desktop application

```bash
python ui.py
```

To run the older terminal version instead:

```bash
python main.py
```

## How to use

- Type a question or command in the message box and press **Send**.
- Press **Voice** and speak after the listening status appears.
- Use the quick-action buttons to open websites, play music, fetch news, or view help.
- Example commands: `open YouTube`, `open Google`, `open GitHub`, `play music`, `news`.
- The app uses Ollama for general AI questions when it is installed and running.

## Important notes

- Voice recognition uses Google's speech-recognition service and therefore requires internet access.
- Ollama runs the language model locally, but the model must be downloaded separately.
- The microphone button listens for one command at a time; it does not run a continuous wake-word listener.
- If microphone access fails, check OS microphone permissions and your audio input device.
- NewsAPI may have plan, country, or request limits.

## Security

Never commit real API keys, passwords, or your `.env` file. Keep secrets in environment variables. If an API key was previously exposed in a source file or ZIP, revoke it and generate a new one. The `.gitignore` excludes local virtual environments, Python cache files, and `.env`.

## Limitations

This project has not been packaged as an installer or deployed as a web service. Feature availability depends on the local Python environment, microphone setup, internet connection, NewsAPI key, and Ollama installation.
