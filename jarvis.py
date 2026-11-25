import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests

try:
    import ollama
except ImportError:
    ollama = None

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
recognizer = sr.Recognizer()


def speak(text):
    """Make Jarvis speak the given text."""
    if not text:
        return
    print("Jarvis:", text)
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        print("Speech Error:", exc)


def ask_ai(prompt):
    if ollama is None:
        return "Ollama is not installed. Install it to use AI chat."
    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a smart AI voice assistant. "
                        "Reply in short, natural sentences suitable for speech. "
                        "Keep answers concise unless the user asks for details."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
    except Exception as exc:
        print("AI Error:", exc)
        return "Sorry, I can't connect to my AI brain right now."


def get_news():
    if not NEWS_API_KEY:
        speak("News API key is not configured.")
        return
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={"country": "us", "apiKey": NEWS_API_KEY},
            timeout=15,
        )
        response.raise_for_status()
        articles = response.json().get("articles", [])[:5]
        speak("Here are today's top headlines.")
        for index, article in enumerate(articles, start=1):
            title = article.get("title")
            if title:
                print(index, title)
                speak(title)
    except requests.RequestException as exc:
        print("News Error:", exc)
        speak("Unable to fetch news.")


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
    "chat gpt": "https://chat.openai.com",
}


def process_command(command):
    command = command.lower().strip()
    if command.startswith("open "):
        site = command[5:].strip()
        if site in WEBSITES:
            speak(f"Opening {site}")
            webbrowser.open(WEBSITES[site])
            return
    if "play music" in command:
        speak("Opening music")
        webbrowser.open("https://www.youtube.com/")
        return
    if "news" in command:
        get_news()
        return
    speak(ask_ai(command))


def main():
    speak("Initializing Jarvis")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Waiting for wake word...")
                audio = recognizer.listen(source)
            wake = recognizer.recognize_google(audio).lower()
            if wake == "jarvis":
                speak("Yes sir")
                while True:
                    try:
                        with sr.Microphone() as source:
                            print("Listening...")
                            recognizer.adjust_for_ambient_noise(source, duration=0.3)
                            audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        print("You:", command)
                        if "stop" in command.lower():
                            speak("Goodbye.")
                            break
                        process_command(command)
                    except sr.UnknownValueError:
                        speak("Please repeat.")
                    except Exception as exc:
                        print("Command Error:", exc)
        except sr.UnknownValueError:
            continue
        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as exc:
            print("Microphone Error:", exc)


if __name__ == "__main__":
    main()
