from core.skill import Skill
import cv2
import os
import time
import requests
import json

class CameraSkill(Skill):
    """
    Nuclear-Grade Robust Camera Skill. 
    Tries every possible hardware backend and index to force a capture on Windows.
    """
    
    @property
    def name(self):
        return "camera_skill"
        
    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "take_photo",
                    "description": "Capture a live photo using the webcam. Automatically detects and selects the best available camera.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sync_to_drive": {
                                "type": "boolean",
                                "description": "Set to true if syncing to Google Drive via N8N is requested."
                            }
                        },
                        "required": [],
                    },
                },
            }
        ]

    def get_functions(self):
        return {
            "take_photo": self.take_photo
        }

    def _attempt_capture(self, index, backend):
        cap = None
        try:
            if backend:
                cap = cv2.VideoCapture(index, backend)
            else:
                cap = cv2.VideoCapture(index)
            
            if not cap.isOpened():
                return None
            
            # Resolution settings for stability
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Warmup is critical backends
            time.sleep(1.5)
            
            # Read multiple frames to clear internal sensor buffer
            for _ in range(5):
                cap.read()
                
            ret, frame = cap.read()
            cap.release()
            
            if ret and frame is not None:
                return frame
            return None
        except:
            if cap:
                cap.release()
            return None

    def take_photo(self, sync_to_drive=False, **kwargs):
        """
        Hyper-robust capture engine.
        """
        save_dir = r"C:\Users\joelm\OneDrive\Desktop\camera photo by lumi"
        os.makedirs(save_dir, exist_ok=True)
        
        frame = None
        used_method = ""

        # Strategy matrix: Index [0, 1] x Backends [DSHOW, MSMF, Default]
        # DSHOW usually works for older/virtual cams, MSMF for modern Win10/11 cams.
        strategies = [
            (0, cv2.CAP_DSHOW, "Index 0 [DSHOW]"),
            (0, cv2.CAP_MSMF, "Index 0 [MSMF]"),
            (1, cv2.CAP_DSHOW, "Index 1 [DSHOW]"),
            (0, None, "Index 0 [Default]"),
            (1, None, "Index 1 [Default]")
        ]

        print(f"  [LUMI Camera] Searching for active sensor...")
        for index, backend, label in strategies:
            print(f"  [LUMI Camera] Trying {label}...")
            frame = self._attempt_capture(index, backend)
            if frame is not None:
                used_method = label
                print(f"  [LUMI Camera] SUCCESS with {label}")
                break
        
        if frame is None:
            return "Error: LUMI could not reach any camera sensor. Please ensure your webcam is connected and the 'Camera Privacy' settings in Windows are turned ON."

        try:
            timestamp = int(time.time())
            filename = f"photo_{timestamp}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            cv2.imwrite(filepath, frame)
            
            status_msg = f"Camera Accessed! Photo captured via {used_method}."

            webhook_url = os.environ.get("N8N_WEBHOOK_URL")
            if (sync_to_drive or "drive" in str(kwargs).lower()) and webhook_url:
                try:
                    payload = {
                        "action": "camera_upload",
                        "data": {
                            "filename": filename,
                            "local_path": filepath,
                            "timestamp": time.ctime(),
                            "user": "Joel"
                        }
                    }
                    requests.post(webhook_url, json=payload, timeout=5)
                    status_msg += " Sent to Google Drive."
                except:
                    status_msg += " (Saved on Desktop, Cloud sync pending)."
            else:
                status_msg += f" Saved to your special Desktop folder."

            return status_msg
            
        except Exception as e:
            return f"Error during image processing: {str(e)}"
