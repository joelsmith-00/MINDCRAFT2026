import cv2
import time

def single_test():
    print("Testing Camera 0 with DSHOW and specific start settings...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Could not open Camera 0.")
        return
    
    print("Camera opened. Setting dimensions...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Warming up...")
    time.sleep(2)
    
    print("Reading frame...")
    ret, frame = cap.read()
    if ret:
        print("Success! Frame captured.")
        cv2.imwrite("single_test.jpg", frame)
    else:
        print("Failed to read frame.")
    
    print("Releasing camera...")
    cap.release()
    print("Done.")

if __name__ == "__main__":
    single_test()
