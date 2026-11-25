"""Core functions for the Jarvis desktop assistant."""
import os
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3

try:
    import ollama
except ImportError:
    ollama = None

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
recognizer = sr.Recognizer()

WEBSITES = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "facebook": "https://facebook.com",
    "linkedin": "https://linkedin.com",
    "github": "https://github.com",
    "instagram": "https://instagram.com",
    "twitter": "https://twitter.com",
    "discord": "https://discord.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "chatgpt": "https://chatgpt.com",
    "chat gpt": "https://chatgpt.com",
}


def speak(text):
    """Speak text aloud. Call from a worker thread, not the Tkinter UI thread."""
    if not text:
        return
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as exc:
        print("Speech error:", exc)


def ask_ai(prompt):
    if ollama is None:
        return "Ollama is not installed. Install Ollama and run: ollama pull llama3.2:3b"
    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful desktop AI assistant. Be clear and concise."},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
    except Exception as exc:
        print("AI error:", exc)
        return "I couldn't connect to Ollama. Check that Ollama is running and llama3.2:3b is installed."


def get_news():
    if not NEWS_API_KEY:
        return ["News is not configured. Add your NewsAPI key as NEWS_API_KEY in your environment."]
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={"country": "in", "apiKey": NEWS_API_KEY},
            timeout=15,
        )
        response.raise_for_status()
        articles = response.json().get("articles", [])[:5]
        return [item.get("title", "") for item in articles if item.get("title")] or ["No headlines were returned."]
    except requests.RequestException as exc:
        print("News error:", exc)
        return ["I couldn't fetch the news. Check your internet connection and API key."]


def handle_command(command):
    """Run one text command and return a response for the UI."""
    cleaned = command.strip()
    lower = cleaned.lower()
    if not lower:
        return "Please enter a command."

    if lower.startswith("open "):
        site = lower[5:].strip()
        if site in WEBSITES:
            webbrowser.open(WEBSITES[site])
            return f"Opening {site.title()}."
        return f"I don't have a website shortcut for '{site}'."

    if "play music" in lower:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube for music."

    if "news" in lower or "headlines" in lower:
        return "\n".join(get_news())

    if lower in {"help", "what can you do"}:
        return (
            "Try: open YouTube, open Google, play music, news, or ask me a question. "
            "Use the microphone button to speak a command."
        )

    return ask_ai(cleaned)
