"""
n8n Webhook Integration Skill for LUMI
Sends tasks and data to n8n workflows
"""

import json
import requests
import re
from typing import List, Dict, Any, Callable
from datetime import datetime as dt_mod
from dateutil import parser as dateparser
from core.skill import Skill


class N8nWebhookSkill(Skill):
    # User's n8n webhook URL (from the request)
    N8N_WEBHOOK_URL = "https://lorderen.app.n8n.cloud/webhook/ai-assistant"

    @property
    def name(self) -> str:
        return "n8n_webhook"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "send_to_n8n",
                    "description": "Send a task or event to n8n for workflow automation (calendar, reminders, integrations)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "intent": {
                                "type": "string",
                                "enum": ["save_calendar", "set_reminder", "send_email", "create_task", "custom"],
                                "description": "Type of task to send to n8n"
                            },
                            "title": {"type": "string", "description": "Title or subject of the task"},
                            "description": {"type": "string", "description": "Detailed description"},
                            "datetime": {"type": "string", "description": "Datetime in format YYYY-MM-DD HH:MM AM/PM"},
                            "details": {"type": "object", "description": "Additional task-specific details"}
                        },
                        "required": ["intent", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_n8n_status",
                    "description": "Check if n8n webhook is reachable",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "send_to_n8n": self.send_to_n8n,
            "check_n8n_status": self.check_n8n_status
        }

    def send_to_n8n(self, intent, title, description=None, datetime=None, details=None):
        """
        Send task data to n8n webhook
        
        Args:
            intent: Type of task (save_calendar, set_reminder, send_email, create_task, custom)
            title: Title of the task
            description: Optional description
            datetime: Optional datetime in format YYYY-MM-DD HH:MM AM/PM
            details: Optional additional details dict
        """
        # Validate datetime before sending
        if datetime:
            # Quick checks: invalid parse or date-only (no time)
            try:
                parsed = dateparser.parse(datetime)
            except Exception:
                return json.dumps({
                    "status": "need_info",
                    "reason": "invalid_datetime",
                    "message": "The provided datetime is invalid. Please provide a valid datetime like '2026-05-07 10:00 AM'."
                })

            # If input appears to be date-only (no time component), ask user whether to create an all-day event or a task
            if not re.search(r"\d{1,2}:\d{2}|am|pm|AM|PM", str(datetime)):
                return json.dumps({
                    "status": "need_info",
                    "reason": "date_only",
                    "message": "The datetime you provided contains only a date. Do you want to save this as an all-day event or as a task? Reply with 'event' or 'task'.",
                    "options": ["event", "task"]
                })

        try:
            payload = {
                "intent": intent,
                "title": title,
                "timestamp": dt_mod.now().isoformat(),
                "user": "Joel"
            }

            if description:
                payload["description"] = description

            if datetime:
                payload["datetime"] = datetime

            if details:
                payload["details"] = details

            # Make POST request to n8n webhook
            response = requests.post(
                self.N8N_WEBHOOK_URL,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 201]:
                message = f"Task '{title}' successfully sent to n8n for {intent}."
                return json.dumps({
                    "status": "success",
                    "message": message,
                    "intent": intent
                })
            else:
                error_msg = f"n8n returned status {response.status_code}"
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to send to n8n: {error_msg}",
                    "status_code": response.status_code
                })

        except requests.exceptions.Timeout:
            return json.dumps({
                "status": "error",
                "message": "n8n webhook request timed out. Check your connection."
            })
        except requests.exceptions.ConnectionError:
            return json.dumps({
                "status": "error",
                "message": "Could not connect to n8n webhook. Verify the URL and your internet connection."
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error sending to n8n: {str(e)}"
            })

    def check_n8n_status(self):
        """Check if n8n webhook is reachable"""
        try:
            response = requests.get(
                self.N8N_WEBHOOK_URL,
                timeout=5
            )
            # n8n webhooks typically return 405 for GET requests, which is OK
            if response.status_code in [200, 201, 405]:
                return json.dumps({
                    "status": "success",
                    "message": "n8n webhook is reachable and ready.",
                    "webhook_url": self.N8N_WEBHOOK_URL
                })
            else:
                return json.dumps({
                    "status": "warning",
                    "message": f"n8n webhook returned status {response.status_code}",
                    "status_code": response.status_code
                })

        except requests.exceptions.ConnectionError:
            return json.dumps({
                "status": "error",
                "message": "Cannot reach n8n webhook. Check your internet and the webhook URL."
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error checking n8n status: {str(e)}"
            })


# Example usage:
# send_to_n8n(
#     intent="save_calendar",
#     title="Meeting with Joel",
#     description="Discuss LUMI updates",
#     datetime="2026-02-26 10:00 AM"
# )
