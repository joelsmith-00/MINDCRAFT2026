import sys
import threading
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

def voice_thread():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ready...")
        audio = r.listen(source)
    print("Heard something!")

app = QApplication(sys.argv)
win = QMainWindow()
lbl = QLabel("Testing Voice and GUI...")
win.setCentralWidget(lbl)
win.show()

t = threading.Thread(target=voice_thread, daemon=True)
t.start()

sys.exit(app.exec())
