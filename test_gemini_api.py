#!/usr/bin/env python3
"""
Quick test script to verify your Gemini API key works
"""

import requests
import json

# Replace with your actual API key
API_KEY = "AIzaSyCIgZbB7zXMsoAE1pLwnHjaNuFlZu1t5D8"

print("Testing Gemini API...\n")

# Try different model versions
models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-1.0-pro"
]

for model in models_to_test:
    print(f"Trying model: {model}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Say hello in one word"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ SUCCESS with {model}!")
            print(f"Response: {result}\n")
            print(f"Use this URL in your code:")
            print(f"url = f\"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={{GEMINI_API_KEY}}\"\n")
            break
        else:
            print(f"❌ Failed: {response.status_code} - {response.text[:100]}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
else:
    print("\n⚠️ None of the models worked. Possible issues:")
    print("1. API key might be invalid or expired")
    print("2. API key might not have Gemini API enabled")
    print("3. You might need to enable the Gemini API in Google Cloud Console")
    print("\nTry:")
    print("- Get a new API key from: https://aistudio.google.com/app/apikey")
    print("- Make sure 'Generative Language API' is enabled")
