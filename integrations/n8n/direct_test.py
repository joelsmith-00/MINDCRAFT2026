import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

def send_test_request():
    # Force the URL regardless of .env for this specific test
    url = "https://lorderen.app.n8n.cloud/webhook/ai-assistant"
    
    payload = {
        "action": "manual_test",
        "data": {
            "message": "Hello n8n! This is a direct request from LUMI.",
            "status": "testing",
            "capability": "webhook_verification"
        },
        "timestamp": datetime.now().isoformat(),
        "user": "Joel"
    }
    
    print(f"--- Sending Request to n8n ---")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=12)
        print(f"\n--- Response from n8n ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS: Request delivered to n8n!")
        else:
            print(f"\n❌ FAILED: Received status {response.status_code}")
            if response.status_code == 404:
                print("Tip: Ensure your n8n workflow is ACTIVE and the path is correct.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    send_test_request()
