from core.skill import Skill
import json
import os

# Safely import WhatsApp client
try:
    from skills.whatsapp.whatsapp_client import WhatsAppClient
    HAS_WHATSAPP = True
except ImportError:
    HAS_WHATSAPP = False

class WhatsappSkill(Skill):
    """
    Skill for sending WhatsApp messages using Selenium and a local contact list.
    """
    
    def __init__(self):
        self.contacts = self._load_contacts()
        self.client = None

    @property
    def name(self):
        return "whatsapp_skill"
        
    def _load_contacts(self):
        contacts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contacts.json")
        try:
            with open(contacts_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"WhatsApp contacts not found (contacts.json): {e}")
            return {}

    def _get_client(self):
        if not self.client:
            if not HAS_WHATSAPP:
                return None
            self.client = WhatsAppClient()
        return self.client

    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Send a WhatsApp message to a specific person by name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the contact (e.g., 'Dad', 'Mom')."
                            },
                            "message": {
                                "type": "string",
                                "description": "The message to send."
                            }
                        },
                        "required": ["name", "message"],
                    },
                },
            }
        ]

    def get_functions(self):
        return {
            "send_whatsapp_message": self.send_whatsapp_message
        }

    def send_whatsapp_message(self, name, message):
        """
        Sends a WhatsApp message to a contact by name.
        """
        if not HAS_WHATSAPP:
            return "Error: WhatsApp client not available. Install selenium and webdriver-manager."
        
        clean_name = name.lower().strip()
        phone_number = self.contacts.get(clean_name)
        
        if not phone_number:
            return f"Error: Contact '{name}' not found in contacts.json. Available: {list(self.contacts.keys())}"
            
        try:
            client = self._get_client()
            if not client:
                return "Error: Could not initialize WhatsApp client."
            result = client.send_message(phone_number, message)
            return result
        except Exception as e:
            return f"Error sending message: {e}"
