import os
import json
from dotenv import load_dotenv
from n8n_skill import N8NSkill

def test_n8n():
    load_dotenv()
    skill = N8NSkill()
    
    print(f"Using Webhook URL: {skill.webhook_url}")
    
    # Test 1: Calendar Event
    print("\n--- Testing Calendar Event ---")
    res1 = skill.create_calendar_event(
        summary="Test Meeting",
        start_time="2026-02-25T10:00:00Z",
        description="Testing N8N integration from LUMI"
    )
    print(res1)
    
    # Test 2: Google Task
    print("\n--- Testing Google Task ---")
    res2 = skill.create_google_task(
        title="Buy Groceries",
        notes="Milk, Eggs, Bread"
    )
    print(res2)
    
    # Test 3: Telegram
    print("\n--- Testing Telegram ---")
    res3 = skill.send_n8n_telegram(
        message="Hello from LUMI test script!"
    )
    print(res3)

if __name__ == "__main__":
    test_n8n()
