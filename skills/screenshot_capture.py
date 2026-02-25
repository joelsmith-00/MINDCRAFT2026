"""
Screenshot Capture Skill - Captures screenshots and saves to OneDrive Desktop
Saves to: C:\\Users\\joelm\\OneDrive\\Desktop\\screenshot by lumi\\{date}_{time}.png
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Callable
from core.skill import Skill

class ScreenshotCaptureSkill(Skill):
    """Skill for capturing screenshots to OneDrive Desktop."""
    
    def __init__(self):
        self.save_dir = r"C:\Users\joelm\OneDrive\Desktop\screenshot by lumi"
        # Create directory if it doesn't exist
        Path(self.save_dir).mkdir(parents=True, exist_ok=True)
    
    @property
    def name(self) -> str:
        return "screenshot_capture_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "capture_screenshot",
                    "description": "Takes a screenshot of the entire desktop and saves it to C:\\\\Users\\\\joelm\\\\OneDrive\\\\Desktop\\\\screenshot by lumi",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "capture_screenshot": self.capture_screenshot
        }

    def capture_screenshot(self) -> str:
        """
        Capture a screenshot and save to the designated folder.
        
        Returns:
            str: Success message with file path or error message
        """
        try:
            from PIL import ImageGrab
        except ImportError:
            return "Error: PIL (Pillow) not installed. Please install it with: pip install Pillow"
        
        try:
            # Generate filename with timestamp
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Save screenshot
            screenshot.save(filepath)
            
            return f"Screenshot captured successfully and saved to {filepath}"
            
        except Exception as e:
            return f"Error capturing screenshot: {str(e)}"
