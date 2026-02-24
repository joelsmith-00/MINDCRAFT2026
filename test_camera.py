import cv2
import os

def test_camera():
    print("Attempting to open camera 0...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera 0 failed. Trying camera 1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Camera 1 failed. Trying camera 2...")
            cap = cv2.VideoCapture(2)
    
    if cap.isOpened():
        print("Camera opened successfully!")
        ret, frame = cap.read()
        if ret:
            save_path = os.path.join(os.getcwd(), "test_photo.jpg")
            cv2.imwrite(save_path, frame)
            print(f"Photo captured and saved to: {save_path}")
        else:
            print("Failed to read frame.")
        cap.release()
    else:
        print("No camera found.")

if __name__ == "__main__":
    test_camera()
