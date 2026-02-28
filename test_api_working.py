#!/usr/bin/env python3
import requests

API_KEY = "AIzaSyCIgZbB7zXMsoAE1pLwnHjaNuFlZu1t5D8"

print("Testing different Gemini API endpoints...\n")

# List of possible working endpoints
endpoints = [
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
    "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
]

payload = {
    "contents": [{"parts": [{"text": "Say 'Hello' in one word"}]}]
}

for i, endpoint in enumerate(endpoints, 1):
    url = f"{endpoint}?key={API_KEY}"
    print(f"[{i}/{len(endpoints)}] Testing: {endpoint.split('/')[-1]}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data['candidates'][0]['content']['parts'][0]['text']
            print(f"  ✅ SUCCESS!")
            print(f"  Response: {result}")
            print(f"\n🎉 Working endpoint found!")
            print(f"\nUse this in your code:")
            print(f'url = f"{endpoint}?key={{GEMINI_API_KEY}}"')
            break
        else:
            print(f"  ❌ Failed: {response.status_code}")
            if response.status_code == 404:
                print(f"     Model not found")
            elif response.status_code == 403:
                print(f"     API key issue or API not enabled")
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:50]}")
    print()
else:
    print("\n⚠️ No working endpoint found!")
    print("\nPossible solutions:")
    print("1. Wait 5-10 minutes after enabling the API")
    print("2. Create a NEW API key at: https://aistudio.google.com/app/apikey")
    print("3. Make sure you clicked 'Create API key in new project'")
