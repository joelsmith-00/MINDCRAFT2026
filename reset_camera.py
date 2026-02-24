import cv2
import time

def release_camera():
    print("Force Releasing Camera Drivers...")
    for i in range(5):
        try:
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            cap.release()
            print(f" Released Index {i}")
        except:
            pass
    print("Reset Complete. Try running LUMI again.")

if __name__ == "__main__":
    release_camera()
