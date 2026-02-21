import speech_recognition as sr
import pyttsx3
import cv2

# Text to speech
engine = pyttsx3.init()
engine.say("System initialized successfully.")
engine.runAndWait()

# Speech recognition test
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except:
    print("Could not understand audio")

# OpenCV test
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    print("Camera working.")
else:
    print("Camera not detected.")

cap.release()
