import os
import json
import subprocess
from typing import List, Dict, Any, Callable
from core.skill import Skill

class SystemSkill(Skill):
    """Full system access skill for Windows — apps, volume, commands, power."""
    
    @property
    def name(self) -> str:
        return "system_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "set_volume",
                    "description": "Set system volume (0-100)",
                    "parameters": { "type": "object", "properties": { "level": {"type": "integer"} }, "required": ["level"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application or program on Windows (e.g. 'notepad', 'chrome', 'calculator', 'explorer')",
                    "parameters": { "type": "object", "properties": { "app_name": {"type": "string"} }, "required": ["app_name"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_system_command",
                    "description": "Run any Windows command/powershell command and return the output. Use this for any system task like listing files, checking system info, network info, disk space, etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "command": {
                                "type": "string",
                                "description": "The PowerShell command to execute"
                            }
                        }, 
                        "required": ["command"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Get system information like CPU, RAM, disk space, OS version, IP address, battery, etc.",
                    "parameters": { "type": "object", "properties": {}, "required": [] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_power",
                    "description": "Shutdown, restart, sleep, or lock the computer",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "action": {
                                "type": "string",
                                "enum": ["shutdown", "restart", "sleep", "lock"],
                                "description": "The power action to perform"
                            }
                        }, 
                        "required": ["action"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "set_volume": self.set_volume,
            "open_app": self.open_app,
            "run_system_command": self.run_system_command,
            "get_system_info": self.get_system_info,
            "control_power": self.control_power,
        }

    def set_volume(self, level):
        try:
            import comtypes
            comtypes.CoInitialize()  # Required when running in a thread
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            level = max(0, min(100, int(level)))
            scalar = level / 100.0
            volume.SetMasterVolumeLevelScalar(scalar, None)
            
            return json.dumps({"status": "success", "level": level})
        except Exception as e:
            # Fallback: use PowerShell to set volume via key simulation
            try:
                level = max(0, min(100, int(level)))
                ps_cmd = f"""
$wshShell = New-Object -ComObject WScript.Shell
# Mute first, then set volume
for ($i = 0; $i -lt 50; $i++) {{ $wshShell.SendKeys([char]174) }}
$steps = [math]::Round({level} / 2)
for ($i = 0; $i -lt $steps; $i++) {{ $wshShell.SendKeys([char]175) }}
"""
                subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=10)
                return json.dumps({"status": "success", "level": level, "method": "fallback"})
            except Exception as e2:
                return json.dumps({"error": f"Volume failed: {str(e)} / fallback: {str(e2)}"})

    def open_app(self, app_name):
        try:
            os.system(f'start "" "{app_name}"')
            return json.dumps({"status": "success", "app": app_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def run_system_command(self, command):
        """Run any system command and return the output."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, timeout=15
            )
            output = result.stdout.strip() if result.stdout else ""
            error = result.stderr.strip() if result.stderr else ""
            
            if error and not output:
                return json.dumps({"status": "error", "output": error})
            return json.dumps({"status": "success", "output": output[:1000]})  # Limit output
        except subprocess.TimeoutExpired:
            return json.dumps({"error": "Command timed out after 15 seconds"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_system_info(self, **kwargs):
        """Get comprehensive system info."""
        try:
            import platform
            info = {
                "os": platform.platform(),
                "processor": platform.processor(),
                "machine": platform.machine(),
                "hostname": platform.node(),
            }
            
            # Get RAM and CPU via PowerShell
            try:
                ram = subprocess.run(
                    ["powershell", "-Command", 
                     "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB, 2)"],
                    capture_output=True, text=True, timeout=5
                )
                info["ram_gb"] = ram.stdout.strip()
            except:
                pass
            
            try:
                cpu = subprocess.run(
                    ["powershell", "-Command", 
                     "(Get-CimInstance Win32_Processor).Name"],
                    capture_output=True, text=True, timeout=5
                )
                info["cpu"] = cpu.stdout.strip()
            except:
                pass
            
            try:
                battery = subprocess.run(
                    ["powershell", "-Command",
                     "(Get-CimInstance Win32_Battery).EstimatedChargeRemaining"],
                    capture_output=True, text=True, timeout=5
                )
                if battery.stdout.strip():
                    info["battery_percent"] = battery.stdout.strip()
            except:
                pass
            
            return json.dumps({"status": "success", "info": info})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def control_power(self, action):
        """Control system power state."""
        try:
            if action == "shutdown":
                os.system("shutdown /s /t 5")
                return json.dumps({"status": "success", "message": "Shutting down in 5 seconds"})
            elif action == "restart":
                os.system("shutdown /r /t 5")
                return json.dumps({"status": "success", "message": "Restarting in 5 seconds"})
            elif action == "sleep":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return json.dumps({"status": "success", "message": "Going to sleep"})
            elif action == "lock":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return json.dumps({"status": "success", "message": "Computer locked"})
            else:
                return json.dumps({"error": f"Unknown action: {action}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
