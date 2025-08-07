import customtkinter as ctk
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import threading
import os
import time


responses = {
    "كيف الطقس اليوم": "جميل جدا امطرت عندنا بغزارة",
    "كيف حالك": "أنا بخير، شكراً لسؤالك!",
    "عرفيني بنفسك": "أنا روبوت محادثة بسيط واسمي نورة ",
    "السلام عليكم معاك البراء": "وعليكم السلام ورحمة الله وبركاته اهلا بك"
}

def bot_response(user_input):
    response = responses.get(user_input.strip(), "لم أفهم، حاول مرة أخرى ")
    insert_message(f"بوت: {response}")
    speak(response)

def speak(text):
    tts = gTTS(text=text, lang='ar')
    filename = f"voice_{int(time.time())}.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def insert_message(message):
    chatbox.configure(state="normal")
    chatbox.insert("end", message + "\n")
    chatbox.configure(state="disabled")
    chatbox.see("end")

def send_text():
    user_input = entry.get().strip()
    if user_input == "":
        return
    insert_message(f"أنت: {user_input}")
    entry.delete(0, 'end')
    threading.Thread(target=bot_response, args=(user_input,)).start()

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        insert_message("\U0001F399 استمع الآن...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ar-SA")
            insert_message(f"أنت (بالمايك): {text}")
            bot_response(text)
        except sr.UnknownValueError:
            insert_message("لم أتمكن من سماعك، حاول مرة أخرى.")
        except sr.RequestError:
            insert_message("خطأ في الاتصال بالإنترنت.")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🤖 المساعد الذكي")
root.geometry("600x700")


chatbox = ctk.CTkTextbox(root, font=("Cairo", 14), width=580, height=500)
chatbox.pack(padx=10, pady=10)
chatbox.configure(state="disabled")


input_frame = ctk.CTkFrame(root)
input_frame.pack(padx=10, pady=10, fill="x")

entry = ctk.CTkEntry(input_frame, font=("Cairo", 14), width=360)
entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
entry.bind("<Return>", lambda e: send_text())

send_btn = ctk.CTkButton(input_frame, text="📨", command=send_text, width=50)
send_btn.pack(side="left")

mic_btn = ctk.CTkButton(input_frame, text="🎤", command=lambda: threading.Thread(target=voice_input).start(), width=50)
mic_btn.pack(side="left", padx=(10, 0))

root.mainloop()
