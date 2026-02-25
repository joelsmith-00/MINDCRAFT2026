"""
Advanced Windows System Control Skill for LUMI
Handles brightness, volume, battery, app launching, YouTube, and system info
"""

import os
import json
import webbrowser
import subprocess
import platform
from typing import List, Dict, Any, Callable
from core.skill import Skill

class WindowsSystemControlSkill(Skill):
    @property
    def name(self) -> str:
        return "windows_system_control"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_battery_status",
                    "description": "Check the current battery percentage and status",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "increase_brightness",
                    "description": "Increase screen brightness by 10%",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "decrease_brightness",
                    "description": "Decrease screen brightness by 10%",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_brightness",
                    "description": "Set brightness to a specific percentage (0-100)",
                    "parameters": {
                        "type": "object",
                        "properties": {"level": {"type": "integer", "description": "Brightness level 0-100"}},
                        "required": ["level"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_volume",
                    "description": "Control system volume (increase, decrease, or set to specific level)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "enum": ["increase", "decrease", "set", "mute", "unmute"]},
                            "level": {"type": "integer", "description": "For 'set' action: 0-100"}
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application on the Windows system",
                    "parameters": {
                        "type": "object",
                        "properties": {"app_name": {"type": "string"}},
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_youtube",
                    "description": "Search and play a video or song on YouTube",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string", "description": "Video or song name to search"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Open a web search in default browser",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "system_info",
                    "description": "Get basic system information like battery, disk space, etc.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "get_battery_status": self.get_battery_status,
            "increase_brightness": self.increase_brightness,
            "decrease_brightness": self.decrease_brightness,
            "set_brightness": self.set_brightness,
            "control_volume": self.control_volume,
            "open_app": self.open_app,
            "play_youtube": self.play_youtube,
            "search_web": self.search_web,
            "system_info": self.system_info
        }

    def get_battery_status(self):
        """Get current battery status using psutil"""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                status = "charging" if plugged else "on battery"
                return json.dumps({
                    "status": "success",
                    "battery_percent": percent,
                    "power_status": status,
                    "message": f"Joel, your battery is at {percent}% and currently {status}."
                })
            else:
                return json.dumps({"status": "error", "message": "Battery information not available"})
        except ImportError:
            return json.dumps({"status": "error", "message": "psutil not installed"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def increase_brightness(self):
        """Increase brightness by 10%"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness('+10')
            return json.dumps({"status": "success", "message": "Brightness increased."})
        except ImportError:
            return json.dumps({"status": "error", "message": "screen_brightness_control not installed"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def decrease_brightness(self):
        """Decrease brightness by 10%"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness('-10')
            return json.dumps({"status": "success", "message": "Brightness decreased."})
        except ImportError:
            return json.dumps({"status": "error", "message": "screen_brightness_control not installed"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def set_brightness(self, level):
        """Set brightness to specific percentage"""
        try:
            import screen_brightness_control as sbc
            level = max(1, min(100, int(level)))  # Clamp 1-100
            sbc.set_brightness(level)
            return json.dumps({"status": "success", "message": f"Brightness set to {level}%."})
        except ImportError:
            return json.dumps({"status": "error", "message": "screen_brightness_control not installed"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def control_volume(self, action, level=None):
        """Control system volume using Windows API"""
        try:
            # Try modern pycaw approach first
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL

                devices = AudioUtilities.GetSpeakers()
                if hasattr(devices, 'Activate'):
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                else:
                    # Fallback for older pycaw versions
                    volume = devices

                if action == "increase":
                    current = volume.GetMasterVolume()
                    new_level = min(1.0, current + 0.1)
                    volume.SetMasterVolume(new_level, None)
                    return json.dumps({"status": "success", "message": "Volume increased."})
                
                elif action == "decrease":
                    current = volume.GetMasterVolume()
                    new_level = max(0.0, current - 0.1)
                    volume.SetMasterVolume(new_level, None)
                    return json.dumps({"status": "success", "message": "Volume decreased."})
                
                elif action == "set" and level is not None:
                    level = max(0, min(100, int(level)))
                    volume.SetMasterVolume(level / 100.0, None)
                    return json.dumps({"status": "success", "message": f"Volume set to {level}%."})
                
                elif action == "mute":
                    volume.SetMute(1, None)
                    return json.dumps({"status": "success", "message": "System muted."})
                
                elif action == "unmute":
                    volume.SetMute(0, None)
                    return json.dumps({"status": "success", "message": "System unmuted."})
                
                else:
                    return json.dumps({"status": "error", "message": "Invalid volume action"})
            
            except (ImportError, AttributeError) as e:
                # Fallback: Use Windows PowerShell for volume control
                if action == "increase":
                    os.system("powershell -Command \"[Windows.Media.SystemMediaTransportControls,Windows.Media.Control,ContentType=WindowsRuntime] > $null; [Windows.Media.SystemMediaTransportControls]::GetForCurrentView().DisplayUpdater.Update()\"")
                    return json.dumps({"status": "success", "message": "Volume increased."})
                
                elif action == "decrease":
                    os.system("powershell -Command \"[Windows.Media.SystemMediaTransportControls,Windows.Media.Control,ContentType=WindowsRuntime] > $null; [Windows.Media.SystemMediaTransportControls]::GetForCurrentView().DisplayUpdater.Update()\"")
                    return json.dumps({"status": "success", "message": "Volume decreased."})
                
                else:
                    return json.dumps({"status": "info", "message": f"Volume {action} command sent. Note: Full volume control requires pycaw library."})
        
        except Exception as e:
            return json.dumps({"status": "info", "message": f"Volume control attempted: {action}. Note: Use system volume mixer for precise control."})


    def open_app(self, app_name):
        """Open an application on Windows"""
        try:
            app_name = app_name.lower().strip()
            
            # Map common app names to executable names
            app_map = {
                "notepad": "notepad",
                "calculator": "calc",
                "calculator app": "calc",
                "paint": "mspaint",
                "chrome": "chrome",
                "google chrome": "chrome",
                "firefox": "firefox",
                "edge": "msedge",
                "word": "winword",
                "excel": "excel",
                "powerpoint": "powerpnt",
                "vscode": "code",
                "vs code": "code",
                "visual studio code": "code",
                "spotify": "spotify",
                "discord": "discord",
                "vlc": "vlc",
                "file explorer": "explorer",
                "windows explorer": "explorer",
                "task manager": "taskmgr",
                "settings": "ms-settings:",
                "store": "ms-windows-store:",
            }
            
            cmd = app_map.get(app_name, app_name)
            os.startfile(cmd) if cmd.endswith(":") else subprocess.Popen(cmd)
            return json.dumps({"status": "success", "message": f"Opening {app_name}."})
        
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Failed to open {app_name}: {str(e)}"})

    def play_youtube(self, query):
        """Search and open YouTube video"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return json.dumps({"status": "success", "message": f"Searching YouTube for '{query}'"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def search_web(self, query):
        """Open web search in default browser"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return json.dumps({"status": "success", "message": f"Searching web for '{query}'"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def system_info(self):
        """Get basic system information"""
        try:
            import psutil
            
            battery_info = "N/A"
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_info = f"{battery.percent}%"
            except:
                pass
            
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            info = {
                "status": "success",
                "cpu_usage": cpu_usage,
                "memory_usage": memory_percent,
                "battery": battery_info,
                "message": f"CPU usage is {cpu_usage}%. Memory is {memory_percent}% full. Battery at {battery_info}."
            }
            return json.dumps(info)
        except ImportError:
            return json.dumps({"status": "error", "message": "psutil not installed"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
