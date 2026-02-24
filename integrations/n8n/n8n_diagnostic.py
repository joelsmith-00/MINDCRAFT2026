import requests
import json
from datetime import datetime

url_prod = "https://lorderen.app.n8n.cloud/webhook/ai-assistant"
url_test = "https://lorderen.app.n8n.cloud/webhook-test/ai-assistant"

payload = {
    "action": "test_connection",
    "data": {"message": "Diagnostic test from LUMI"},
    "timestamp": datetime.now().isoformat(),
    "user": "Joel"
}

def try_url(url, name):
    print(f"\n--- Testing {name} URL: {url} ---")
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    s1 = try_url(url_prod, "Production")
    s2 = try_url(url_test, "Test")
    
    if s1 == 200 or s2 == 200:
        print("\n✅ SUCCESS: N8N is receiving data!")
    else:
        print("\n❌ FAILED: N8N returned 404. Please check if the Webhook is 'Activated' in your n8n workflow.")
