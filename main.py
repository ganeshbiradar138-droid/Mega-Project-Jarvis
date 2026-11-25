import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests

recognizer = sr.Recognizer()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def process_command(command):
    command = command.lower()
    websites = {
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "youtube": "https://youtube.com",
        "linkedin": "https://linkedin.com",
        "github": "https://github.com",
        "whatsapp": "https://web.whatsapp.com",
        "instagram": "https://instagram.com",
        "twitter": "https://twitter.com",
        "steam": "https://store.steampowered.com",
        "discord": "https://discord.com",
        "gmail": "https://mail.google.com",
        "ai": "https://chat.openai.com",
    }
    for name, url in websites.items():
        if f"open {name}" in command:
            speak(f"Opening {name}")
            webbrowser.open(url)
            return
    if "play music" in command:
        speak("Opening music")
        webbrowser.open("https://www.youtube.com/")
        return
    if "news" in command:
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
            for article in response.json().get("articles", [])[:5]:
                if article.get("title"):
                    speak(article["title"])
        except requests.RequestException as exc:
            print("News Error:", exc)
            speak("Unable to fetch news.")
        return
    speak("Sorry, I didn't understand that command.")


if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes sir")
                while True:
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        if "stop" in command.lower():
                            speak("Okay, stopping now.")
                            break
                        process_command(command)
                    except sr.UnknownValueError:
                        speak("I didn't catch that, please repeat.")
        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as exc:
            print("Error:", exc)
