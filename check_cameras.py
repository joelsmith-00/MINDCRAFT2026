import cv2

def check_cameras():
    print("DirectShow (CAP_DSHOW) Testing:")
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"  [DSHOW] Camera {i} is available")
            cap.release()
        else:
            print(f"  [DSHOW] Camera {i} not found")

    print("\nMedia Foundation (CAP_MSMF) Testing:")
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
        if cap.isOpened():
            print(f"  [MSMF] Camera {i} is available")
            cap.release()
        else:
            print(f"  [MSMF] Camera {i} not found")

if __name__ == "__main__":
    check_cameras()
