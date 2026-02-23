import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class FileSkill(Skill):
    """Full filesystem access — read, write, create, list files anywhere on the system."""
    
    @property
    def name(self) -> str:
        return "file_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "manage_file",
                    "description": "Read, write, create, or append to any file on the system. Can access any path.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["read", "write", "create", "append"],
                                "description": "The file operation to perform"
                            },
                            "filepath": {
                                "type": "string",
                                "description": "Full file path (e.g. 'C:/Users/joelm/Desktop/notes.txt' or '~/Documents/file.txt')"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write (for write/create/append actions)"
                            }
                        },
                        "required": ["action", "filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List all files and folders in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Directory path to list (e.g. 'C:/Users/joelm/Desktop')"
                            }
                        },
                        "required": ["path"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "manage_file": self.manage_file,
            "list_directory": self.list_directory
        }

    def manage_file(self, action, filepath, content=""):
        try:
            # Expand user paths like ~
            filepath = os.path.expanduser(filepath)
            
            if action == "read":
                with open(filepath, "r", encoding="utf-8") as f:
                    data = f.read(5000)  # Limit to 5000 chars
                return json.dumps({"status": "success", "content": data})
            
            elif action == "write" or action == "create":
                os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return json.dumps({"status": "success", "message": f"File written: {filepath}"})
            
            elif action == "append":
                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(content)
                return json.dumps({"status": "success", "message": f"Content appended to: {filepath}"})
            
            else:
                return json.dumps({"error": f"Unknown action: {action}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_directory(self, path):
        try:
            path = os.path.expanduser(path)
            items = []
            for item in os.listdir(path)[:50]:  # Limit to 50 items
                full = os.path.join(path, item)
                items.append({
                    "name": item,
                    "type": "folder" if os.path.isdir(full) else "file",
                    "size": os.path.getsize(full) if os.path.isfile(full) else None
                })
            return json.dumps({"status": "success", "path": path, "items": items})
        except Exception as e:
            return json.dumps({"error": str(e)})
