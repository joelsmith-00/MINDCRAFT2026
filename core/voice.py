import os
import sys
import speech_recognition as sr

# Global flag
is_speaking = False

def speak(text):
    """Speak text using a fresh pyttsx3 engine each time (thread-safe)."""
    global is_speaking
    
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
    
    print(f"LUMI: {text}")
    is_speaking = True
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Use David voice on Windows (male)
        for v in voices:
            if "david" in v.name.lower():
                engine.setProperty('voice', v.id)
                break
        engine.setProperty('rate', 190)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        is_speaking = False

def listen():
    """Listen for voice input."""
    global is_speaking
    if is_speaking:
        return "none"

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.8
            r.energy_threshold = 400
            r.dynamic_energy_threshold = True
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source, timeout=6, phrase_time_limit=12)
                print("Recognizing...")
                query = r.recognize_google(audio)
                print(f"You said: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                return "none"
            except sr.UnknownValueError:
                return "none"
            except sr.RequestError as e:
                print(f"Speech API Error: {e}")
                return "none"
            except Exception:
                return "none"
    except Exception as e:
        print(f"Mic Error: {e}")
        try:
            user_input = input("YOU (type): ").strip()
            return user_input.lower() if user_input else "none"
        except (EOFError, KeyboardInterrupt):
            return "none"
