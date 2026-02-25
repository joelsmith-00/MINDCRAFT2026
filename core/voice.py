import os
import sys
import pyttsx3
import speech_recognition as sr  # (Optional: can be removed if not used elsewhere)
import whisper
from vosk import Model, KaldiRecognizer

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# PyAudio availability check
PYAUDIO_AVAILABLE = False
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pass

# Set voice to deep male voice
def set_deep_male_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        # Prefer "David" for Windows male voice
        if "David" in voice.name:
            engine.setProperty('voice', voice.id)
            return
    # Fallback to any male voice if David not found
    for voice in voices:
        if "male" in voice.name.lower() or "male" in str(voice.gender).lower():
             engine.setProperty('voice', voice.id)
             return

set_deep_male_voice()

# Global flag to check if Lumi is speaking
is_speaking = False

def speak(text):
    global is_speaking
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
    
    # Print first so user sees it even if audio fails
    print(f"LUMI: {text}")

    # Set flag to True before speaking
    is_speaking = True
    
    try:
        # On Windows, use SAPI (built-in)
        if sys.platform == "win32":
            try:
                engine.say(text)
                engine.runAndWait()
                return
            except Exception as e:
                return
        
        # On macOS, use 'say' command
        if sys.platform == "darwin":
            try:
                clean_text = text.replace('"', '\\"').replace("'", "")
                os.system(f'say "{clean_text}"')
                return
            except Exception:
                return
        
        # Fallback: try pyttsx3
        engine.say(text)
        engine.runAndWait()
            
    except Exception:
        pass
    finally:
        is_speaking = False

def listen():
    """Listen for voice input using Google Speech Recognition"""
    global is_speaking
    
    # if system is speaking, don't listen
    if is_speaking:
        return "none"
    
    # Check if PyAudio is available
    if not PYAUDIO_AVAILABLE:
        print("\n" + "=" * 70)
        print("AUDIO ERROR - PyAudio is not installed!")
        print("=" * 70)
        print("\nMicrophone input requires PyAudio on Windows.")
        print("\n[FIX 1] Install PyAudio:")
        print("  python -m pip install PyAudio --upgrade")
        print("\n[FIX 2] Use TEXT MODE (Recommended):")
        print("  python main.py --text")
        print("\n[FIX 3] Use WEB MODE:")
        print("  Open: http://localhost:5000")
        print("=" * 70 + "\n")
        return "none"

    try:
        import sounddevice as sd
        import numpy as np
        import tempfile
        import scipy.io.wavfile as wav
        print("Listening (Whisper)...")
        samplerate = 16000
        duration = 8  # seconds
        print("Speak now...")
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        # Save to temp WAV file
        import time
        import uuid
        temp_wav = os.path.join(os.getcwd(), f"lumi_voice_{uuid.uuid4().hex}.wav")
        # Set language: 'en' for English, 'ta' for Tamil
        vosk_lang = "en"  # Change to "ta" for Tamil
        try:
            # Flatten audio array for mono
            audio_flat = audio.flatten()
            wav.write(temp_wav, samplerate, audio_flat)
            time.sleep(0.15)
            if not os.path.exists(temp_wav):
                print("Temp WAV file was not created or found!")
                return "none"
            print(f"Recognizing (Vosk {vosk_lang})...")
            import urllib.request, zipfile
            if vosk_lang == "en":
                vosk_model_dir = "vosk-model-small-en-us-0.15"
                vosk_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
            elif vosk_lang == "ta":
                vosk_model_dir = "vosk-model-small-ta-0.4"
                vosk_url = "https://alphacephei.com/vosk/models/vosk-model-small-ta-0.4.zip"
            else:
                print(f"Unsupported language: {vosk_lang}")
                return "none"
            if not os.path.exists(vosk_model_dir):
                print(f"Downloading Vosk model for {vosk_lang}...")
                zip_path = f"{vosk_model_dir}.zip"
                urllib.request.urlretrieve(vosk_url, zip_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(".")
                os.remove(zip_path)
            vosk_model = Model(vosk_model_dir)
            rec = KaldiRecognizer(vosk_model, samplerate)
            import wave
            wf = wave.open(temp_wav, "rb")
            data = wf.readframes(wf.getnframes())
            if rec.AcceptWaveform(data):
                result = rec.Result()
                import json
                text = json.loads(result).get("text", "").strip()
                if text:
                    return text.lower()
            print(f"Could not understand audio with Vosk ({vosk_lang}).")
            return "none"
        except Exception as vosk_error:
            print(f"Vosk failed: {vosk_error}")
            return "none"
        finally:
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except Exception:
                    pass
    except Exception as e:
        print(f"Voice Error (Whisper): {type(e).__name__}: {e}")
        return "none"
