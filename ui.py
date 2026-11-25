"""Jarvis desktop UI built with Tkinter (no extra UI framework required)."""
import queue
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

import speech_recognition as sr

from jarvis import handle_command, speak, recognizer


class JarvisApp:
    BG = "#0b1020"
    PANEL = "#121a2e"
    PANEL_2 = "#18233b"
    TEXT = "#e8eefc"
    MUTED = "#91a1bf"
    ACCENT = "#54d6ff"
    GREEN = "#51e0a2"

    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS | Personal AI Assistant")
        self.root.geometry("1000x720")
        self.root.minsize(760, 600)
        self.root.configure(bg=self.BG)
        self.events = queue.Queue()
        self.busy = False
        self._build_ui()
        self.root.after(100, self._poll_events)
        self.add_message("JARVIS", "Systems online. How can I help you?", "assistant")

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=28, pady=(22, 14))
        brand = tk.Frame(header, bg=self.BG)
        brand.pack(side="left")
        tk.Label(brand, text="◉  J.A.R.V.I.S", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(brand, text="PERSONAL AI • DESKTOP INTERFACE", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(3, 0))
        self.status = tk.Label(header, text="● READY", bg=self.PANEL, fg=self.GREEN,
                               font=("Segoe UI", 9, "bold"), padx=14, pady=9)
        self.status.pack(side="right")

        hero = tk.Frame(self.root, bg=self.PANEL, highlightthickness=1, highlightbackground="#263653")
        hero.pack(fill="x", padx=28, pady=(0, 16))
        hero_inner = tk.Frame(hero, bg=self.PANEL)
        hero_inner.pack(fill="x", padx=20, pady=17)
        tk.Label(hero_inner, text="GOOD DAY.", bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(hero_inner, text="What are we working on?", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(4, 2))
        tk.Label(hero_inner, text="Ask a question, launch a website, or use voice input.",
                 bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 10)).pack(anchor="w")

        content = tk.Frame(self.root, bg=self.BG)
        content.pack(fill="both", expand=True, padx=28, pady=(0, 14))
        chat_panel = tk.Frame(content, bg=self.PANEL, highlightthickness=1, highlightbackground="#263653")
        chat_panel.pack(side="left", fill="both", expand=True)
        chat_header = tk.Frame(chat_panel, bg=self.PANEL)
        chat_header.pack(fill="x", padx=18, pady=14)
        tk.Label(chat_header, text="CONVERSATION", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(chat_header, text="LOCAL SESSION", bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="right")

        self.chat = tk.Text(chat_panel, bg=self.PANEL, fg=self.TEXT, insertbackground=self.TEXT,
                            relief="flat", wrap="word", padx=18, pady=8,
                            font=("Segoe UI", 10), state="disabled", spacing1=5, spacing3=12)
        self.chat.pack(fill="both", expand=True, padx=4, pady=(0, 10))
        self.chat.tag_configure("assistant", foreground=self.ACCENT, font=("Segoe UI", 9, "bold"))
        self.chat.tag_configure("user", foreground=self.GREEN, font=("Segoe UI", 9, "bold"))
        self.chat.tag_configure("body", foreground=self.TEXT, lmargin1=4, lmargin2=4)
        self.chat.tag_configure("time", foreground=self.MUTED, font=("Segoe UI", 8))

        side = tk.Frame(content, bg=self.BG, width=220)
        side.pack(side="right", fill="y", padx=(14, 0))
        side.pack_propagate(False)
        tk.Label(side, text="QUICK ACTIONS", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 10))
        for label, command in [
            ("⌕  Search with Google", "open Google"),
            ("▶  Open YouTube", "open YouTube"),
            ("◉  Open GitHub", "open GitHub"),
            ("♫  Play music", "play music"),
            ("▤  Top news", "news"),
            ("?  Help", "help"),
        ]:
            btn = tk.Button(side, text=label, command=lambda c=command: self.submit(c),
                            bg=self.PANEL_2, fg=self.TEXT, activebackground="#263653",
                            activeforeground=self.TEXT, relief="flat", anchor="w",
                            padx=12, pady=12, cursor="hand2", font=("Segoe UI", 9))
            btn.pack(fill="x", pady=4)

        composer = tk.Frame(self.root, bg=self.PANEL, highlightthickness=1, highlightbackground="#263653")
        composer.pack(fill="x", padx=28, pady=(0, 24))
        self.entry = tk.Entry(composer, bg=self.PANEL, fg=self.TEXT, insertbackground=self.TEXT,
                              relief="flat", font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, padx=(16, 8), pady=16)
        self.entry.insert(0, "Type a message or command...")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<Return>", lambda _event: self.send_text())
        tk.Button(composer, text="🎙  VOICE", command=self.listen,
                  bg=self.PANEL_2, fg=self.ACCENT, activebackground="#263653",
                  relief="flat", padx=13, pady=10, cursor="hand2",
                  font=("Segoe UI", 9, "bold")).pack(side="right", padx=5, pady=7)
        tk.Button(composer, text="SEND  ➤", command=self.send_text,
                  bg=self.ACCENT, fg="#07111f", activebackground="#8be6ff",
                  relief="flat", padx=16, pady=10, cursor="hand2",
                  font=("Segoe UI", 9, "bold")).pack(side="right", padx=(5, 9), pady=7)

    def _clear_placeholder(self, _event):
        if self.entry.get() == "Type a message or command...":
            self.entry.delete(0, "end")

    def add_message(self, who, message, kind):
        self.chat.configure(state="normal")
        self.chat.insert("end", who + "  ", kind)
        self.chat.insert("end", datetime.now().strftime("%H:%M") + "\n", "time")
        self.chat.insert("end", message + "\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def send_text(self):
        command = self.entry.get().strip()
        if not command or command == "Type a message or command..." or self.busy:
            return
        self.entry.delete(0, "end")
        self.add_message("YOU", command, "user")
        self._run_command(command)

    def submit(self, command):
        if self.busy:
            return
        self.add_message("YOU", command, "user")
        self._run_command(command)

    def _run_command(self, command):
        self._set_busy(True, "PROCESSING")
        def work():
            try:
                answer = handle_command(command)
                self.events.put(("reply", answer))
                if answer:
                    speak(answer.replace("\n", ". "))
            except Exception as exc:
                self.events.put(("reply", f"Something went wrong: {exc}"))
            finally:
                self.events.put(("ready", None))
        threading.Thread(target=work, daemon=True).start()

    def listen(self):
        if self.busy:
            return
        self._set_busy(True, "LISTENING")
        def work():
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.events.put(("status", "LISTENING — SPEAK NOW"))
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=12)
                text = recognizer.recognize_google(audio)
                self.events.put(("heard", text))
                answer = handle_command(text)
                self.events.put(("reply", answer))
                if answer:
                    speak(answer.replace("\n", ". "))
            except sr.WaitTimeoutError:
                self.events.put(("reply", "I didn't hear anything. Press Voice and try again."))
            except sr.UnknownValueError:
                self.events.put(("reply", "I couldn't understand that. Please try again."))
            except Exception as exc:
                self.events.put(("reply", f"Voice input error: {exc}"))
            finally:
                self.events.put(("ready", None))
        threading.Thread(target=work, daemon=True).start()

    def _set_busy(self, busy, label=None):
        self.busy = busy
        self.status.configure(text=("● " + (label or "WORKING")) if busy else "● READY",
                              fg=self.ACCENT if busy else self.GREEN)

    def _poll_events(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "heard":
                    self.add_message("YOU (VOICE)", value, "user")
                elif kind == "reply":
                    self.add_message("JARVIS", value, "assistant")
                elif kind == "status":
                    self.status.configure(text="● " + value, fg=self.ACCENT)
                elif kind == "ready":
                    self._set_busy(False)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_events)


if __name__ == "__main__":
    window = tk.Tk()
    app = JarvisApp(window)
    window.mainloop()
