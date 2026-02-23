import os
import json
import requests
from typing import List, Dict, Any, Callable
from core.skill import Skill

class N8NSkill(Skill):
    """Skill for triggering N8N workflows for calendar, tasks, and telegram."""
    
    def __init__(self):
        self.webhook_url = os.environ.get("N8N_WEBHOOK_URL")
        # Fallback to a placeholder if not set
        if not self.webhook_url:
            self.webhook_url = "https://n8n.cloud/webhook/your-webhook-id"

    @property
    def name(self) -> str:
        return "n8n_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_calendar_event",
                    "description": "Create a new event in Google Calendar using N8N",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "The title of the event"},
                            "start_time": {"type": "string", "description": "Start time of the event (ISO 8601 format)"},
                            "end_time": {"type": "string", "description": "End time of the event (ISO 8601 format)"},
                            "description": {"type": "string", "description": "Description of the event"}
                        },
                        "required": ["summary", "start_time"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_google_task",
                    "description": "Create a new task in Google Tasks using N8N",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "notes": {"type": "string", "description": "Additional notes for the task"},
                            "due_date": {"type": "string", "description": "Optional due date for the task"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_n8n_telegram",
                    "description": "Send a message via Telegram using N8N",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "The message to send"},
                            "chat_id": {"type": "string", "description": "Optional specific chat ID"}
                        },
                        "required": ["message"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "create_calendar_event": self.create_calendar_event,
            "create_google_task": self.create_google_task,
            "send_n8n_telegram": self.send_n8n_telegram
        }

    def _trigger_webhook(self, action: str, data: Dict[str, Any]) -> str:
        """Helper to send data to the N8N webhook."""
        if not self.webhook_url or "your-webhook-id" in self.webhook_url:
            return json.dumps({
                "status": "error",
                "message": "N8N Webhook URL not configured in .env file"
            })
            
        payload = {
            "action": action,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "user": "Joel"
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            if response.status_code >= 200 and response.status_code < 300:
                return json.dumps({
                    "status": "success",
                    "message": f"Successfully triggered N8N for {action}",
                    "n8n_response": response.text
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"N8N returned status code {response.status_code}",
                    "details": response.text
                })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to trigger N8N: {str(e)}"
            })

    def create_calendar_event(self, summary: str, start_time: str, end_time: str = None, description: str = "") -> str:
        """Trigger N8N to create a calendar event."""
        data = {
            "summary": summary,
            "start_time": start_time,
            "end_time": end_time,
            "description": description
        }
        return self._trigger_webhook("create_calendar_event", data)

    def create_google_task(self, title: str, notes: str = "", due_date: str = None) -> str:
        """Trigger N8N to create a Google task."""
        data = {
            "title": title,
            "notes": notes,
            "due_date": due_date
        }
        return self._trigger_webhook("create_task", data)

    def send_n8n_telegram(self, message: str, chat_id: str = None) -> str:
        """Trigger N8N to send a Telegram message."""
        data = {
            "message": message,
            "chat_id": chat_id
        }
        return self._trigger_webhook("send_telegram", data)
