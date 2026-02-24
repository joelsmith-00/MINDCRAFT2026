import os
import json
import requests
from datetime import datetime
from n8n_skill import N8NSkill
from dotenv import load_dotenv

def force_event():
    load_dotenv()
    skill = N8NSkill()
    
    print(f"Triggering N8N at: {skill.webhook_url}")
    
    # Specific request for March 1st 2026 at 10:00 AM
    res = skill.create_calendar_event(
        summary="March 1st Meeting",
        start_time="2026-03-01T10:00:00",
        description="Event created via LUMI forced test"
    )
    
    print("\n--- Response ---")
    print(res)

if __name__ == "__main__":
    force_event()
