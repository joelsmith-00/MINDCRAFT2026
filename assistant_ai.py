import requests
import pyttsx3
import speech_recognition as sr

OPENROUTER_API_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"

engine = pyttsx3.init()

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text
    except:
        return None

chat_history = []

def ask_ai(user_text):

    chat_history.append({"role": "user", "content": user_text})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """
You are an AI assistant.
Return ONLY JSON.
Do not explain.
Maintain context from previous messages.

Structure:
{
  "intent": "",
  "message": "",
  "time": ""
}

Allowed intents:
- general_chat
- set_reminder
- send_message
- make_call
"""
                }
            ] + chat_history
        }
    )

    result = response.json()
    reply = result["choices"][0]["message"]["content"]

    chat_history.append({"role": "assistant", "content": reply})

    return reply

while True:
    user_input = listen()

    if user_input:
        if "exit" in user_input.lower():
            speak("Goodbye Joel.")
            break

        reply = ask_ai(user_input)
        speak(reply)
