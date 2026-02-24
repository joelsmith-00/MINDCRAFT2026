"""
LUMI Wake Word Listener
========================
Runs in the background, listening for "Hey Lumi".
When detected, launches the full LUMI AI Assistant with GUI.
"""

import os
import sys
import subprocess
import time
import speech_recognition as sr

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = os.path.join(PROJECT_DIR, "venv", "Scripts", "python.exe")
MAIN_SCRIPT = os.path.join(PROJECT_DIR, "main.py")

def launch_lumi():
    """Launch the full LUMI app with GUI in a new console window."""
    print("\n🚀 LAUNCHING LUMI!\n")
    
    # Play a beep to confirm
    try:
        import winsound
        winsound.Beep(800, 200)
        winsound.Beep(1000, 200)
    except:
        pass
    
    proc = subprocess.Popen(
        [PYTHON_EXE, MAIN_SCRIPT],
        cwd=PROJECT_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    # Wait for LUMI to exit before listening again
    print("[LISTENER] LUMI is running. Waiting for it to close...")
    proc.wait()
    print("[LISTENER] LUMI closed. Listening for wake word again...\n")

def listen_for_wake_word():
    r = sr.Recognizer()
    
    print("=" * 50)
    print("  🎤 LUMI WAKE WORD LISTENER ACTIVE")
    print("  Say 'Hey Lumi' to start!")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)
    
    # Calibrate once on start
    print("\n[LISTENER] Calibrating microphone...")
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            r.energy_threshold = max(r.energy_threshold, 300)
    except Exception as e:
        print(f"[LISTENER] Mic error: {e}")
        return
    
    print(f"[LISTENER] Ready! Energy threshold: {r.energy_threshold}")
    print("[LISTENER] Waiting for 'Hey Lumi'...\n")
    
    r.pause_threshold = 0.6
    r.dynamic_energy_threshold = True
    
    while True:
        try:
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source, timeout=8, phrase_time_limit=4)
                except sr.WaitTimeoutError:
                    continue
                
                try:
                    text = r.recognize_google(audio).lower().strip()
                    print(f"  Heard: '{text}'")
                    
                    # Check for wake word — flexible matching (includes common mishearings)
                    wake_words = ["hey", "lumi", "loomy", "lumy", "loomi", "luminee", "lummi",
                                  "mummy", "rumi", "bloomy", "gloomy", "dummy",
                                  "loo me", "lu mi", "loo mi", "illumi", "plumi",
                                  "bhoomi", "bhoomy", "boomy", "boomi", "bhumi",
                                  "tommy", "tummy", "yummy", "humi", "gumi"]
                    if any(w in text for w in wake_words):
                        launch_lumi()
                    
                except sr.UnknownValueError:
                    pass  # Couldn't understand — keep listening
                except sr.RequestError as e:
                    print(f"[LISTENER] API error: {e}")
                    time.sleep(3)
                    
        except KeyboardInterrupt:
            print("\n[LISTENER] Stopped.")
            break
        except Exception as e:
            print(f"[LISTENER] Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    listen_for_wake_word()
