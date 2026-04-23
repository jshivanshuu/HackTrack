import requests
import time
import random

API_URL = "http://127.0.0.1:8000/api/v1/ingest"
API_KEY = "test_api_key"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

payloads = [
    {"ip_address": "192.168.1.10", "endpoint": "/login", "method": "POST", "payload": "username=admin&password=123", "headers": "User-Agent: Mozilla/5.0"}, # Normal
    {"ip_address": "10.0.0.5", "endpoint": "/search", "method": "GET", "payload": "q=' OR 1=1 --", "headers": "User-Agent: curl/7.68.0"}, # SQLi
    {"ip_address": "45.22.11.9", "endpoint": "/profile", "method": "POST", "payload": "bio=<script>alert('xss')</script>", "headers": "User-Agent: Mozilla"}, # XSS
    {"ip_address": "192.168.1.105", "endpoint": "/dashboard", "method": "GET", "payload": "", "headers": "User-Agent: Chrome"}, # Normal
]

print("Starting traffic simulation to HackTrack...")

for i in range(10):
    log_data = random.choice(payloads)
    try:
        response = requests.post(API_URL, json=log_data, headers=headers)
        print(f"Sent {log_data['method']} {log_data['endpoint']} - Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Failed to connect. Is the FastAPI server running?")
    time.sleep(2)

print("Done.")

# Note: Before running this, you need to create an APIKey in the database!
