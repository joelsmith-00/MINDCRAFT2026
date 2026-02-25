"""
Camera Photo Capture Skill - Captures photos from webcam and saves to OneDrive Desktop
Saves to: C:\\Users\\joelm\\OneDrive\\Desktop\\camera photo by lumi\\{date}_{time}.jpg
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Callable
from core.skill import Skill

class CameraCaptureSkill(Skill):
    """Skill for capturing photos from webcam to OneDrive Desktop."""
    
    def __init__(self):
        self.save_dir = r"C:\Users\joelm\OneDrive\Desktop\camera photo by lumi"
        # Create directory if it doesn't exist
        Path(self.save_dir).mkdir(parents=True, exist_ok=True)
    
    @property
    def name(self) -> str:
        return "camera_capture_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "capture_photo_from_camera",
                    "description": "Takes a photo from your webcam and saves it to C:\\\\Users\\\\joelm\\\\OneDrive\\\\Desktop\\\\camera photo by lumi",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "capture_photo_from_camera": self.capture_photo_from_camera
        }

    def capture_photo_from_camera(self) -> str:
        """
        Capture a photo from the webcam and save to the designated folder.
        
        Returns:
            str: Success message with file path or error message
        """
        try:
            import cv2
        except ImportError:
            return "Error: OpenCV (cv2) not installed. Install with: pip install opencv-python"
        
        try:
            # Generate filename with timestamp
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"photo_{timestamp}.jpg"
            filepath = os.path.join(self.save_dir, filename)
            
            # Open webcam
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return "Error: Could not access webcam. Please check if camera is connected and not in use by another application."
            
            # Capture a single frame
            ret, frame = cap.read()
            
            # Release the camera
            cap.release()
            
            if not ret:
                return "Error: Failed to capture frame from webcam."
            
            # Save the photo
            cv2.imwrite(filepath, frame)
            
            return f"Photo captured successfully from camera and saved to {filepath}"
            
        except Exception as e:
            return f"Error capturing photo from camera: {str(e)}"
