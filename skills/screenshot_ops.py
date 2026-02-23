import os
import json
from datetime import datetime
from typing import List, Dict, Any, Callable
from core.skill import Skill

class ScreenshotSkill(Skill):
    """Skill for taking screenshots on Windows."""
    
    def __init__(self):
        # Screenshot directory on Desktop
        self.screenshot_dir = r"C:\Users\joelm\OneDrive\Desktop\screenshot by lumi"
        # Create directory if it doesn't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    @property
    def name(self) -> str:
        return "screenshot_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "take_screenshot",
                    "description": "Take a screenshot of the entire screen and save it to a file. Returns the path to the saved screenshot.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Optional custom filename for the screenshot (without extension). If not provided, uses timestamp."
                            }
                        },
                        "required": []
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "take_screenshot": self.take_screenshot
        }

    def take_screenshot(self, filename: str = None) -> str:
        """
        Take a screenshot using Pillow ImageGrab (Windows compatible).
        
        Args:
            filename: Optional custom filename (without extension)
            
        Returns:
            JSON string with status and filepath
        """
        try:
            from PIL import ImageGrab
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}"
            
            # Ensure .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Take screenshot using Pillow
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            
            if os.path.exists(filepath):
                return json.dumps({
                    "status": "success",
                    "message": "Screenshot saved successfully",
                    "path": filepath
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": "Failed to save screenshot"
                })
                
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Screenshot error: {str(e)}"
            })
