#!/usr/bin/env python3
"""
AI-Powered WhatsApp Chatbot using Google Gemini
================================================
This version uses Google's Gemini AI for intelligent responses.

Setup:
1. Get your free Gemini API key from: https://makersuite.google.com/app/apikey
2. Replace YOUR_API_KEY_HERE below with your actual key
3. Run: python whatsapp_ai_chatbot.py --test
"""

import requests
import json
import sys
from typing import Optional

# =============================================================================
# CONFIGURATION - REPLACE WITH YOUR ACTUAL API KEY
# =============================================================================

GEMINI_API_KEY = "AIzaSyCIgZbB7zXMsoAE1pLwnHjaNuFlZu1t5D8"  # Get from: https://makersuite.google.com/app/apikey

# Alternative: Use OpenAI ChatGPT instead
# Uncomment and add your OpenAI key if you prefer ChatGPT
# OPENAI_API_KEY = "YOUR_OPENAI_KEY_HERE"
# USE_OPENAI = False  # Set to True to use ChatGPT instead of Gemini

# =============================================================================
# AI RESPONSE FUNCTIONS
# =============================================================================

def get_gemini_response(user_message: str) -> str:
    """
    Get AI response from Google Gemini.
    
    Args:
        user_message: The user's message
        
    Returns:
        AI-generated response
    """
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return "⚠️ ERROR: Please add your Gemini API key in the script!\n\nGet it from: https://makersuite.google.com/app/apikey"
    
    # Correct Gemini API endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    
    # System prompt for the chatbot personality
    prompt = f"""You are a helpful and friendly WhatsApp chatbot assistant.

Rules:
1. Detect the language of the user's message and respond in THE SAME LANGUAGE
2. Be conversational, warm, and helpful
3. Keep responses concise (2-3 sentences for casual chat, longer for complex questions)
4. If user asks questions, provide accurate and helpful answers
5. Match the user's tone and style
6. Use emojis occasionally to be friendly 😊

User message: {user_message}

Respond naturally:"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        ai_response = data['candidates'][0]['content']['parts'][0]['text']
        return ai_response.strip()
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "403" in error_msg or "API_KEY_INVALID" in error_msg:
            return "❌ API Key Error: Your Gemini API key is invalid. Please check it at https://makersuite.google.com/app/apikey"
        elif "429" in error_msg:
            return "⏳ Rate limit exceeded. Please wait a moment and try again."
        else:
            return f"❌ Error connecting to AI: {error_msg}\n\nPlease check your internet connection and API key."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


def get_chatgpt_response(user_message: str) -> str:
    """
    Get AI response from OpenAI ChatGPT (alternative to Gemini).
    
    Args:
        user_message: The user's message
        
    Returns:
        AI-generated response
    """
    # Uncomment this if you want to use ChatGPT instead
    """
    if OPENAI_API_KEY == "YOUR_OPENAI_KEY_HERE":
        return "⚠️ ERROR: Please add your OpenAI API key!"
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful WhatsApp chatbot. Be friendly and concise."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ ChatGPT Error: {str(e)}"
    """
    return "ChatGPT integration is commented out. Uncomment the code above to use it."


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def generate_ai_response(message: str) -> str:
    """
    Main function to generate AI response.
    
    Args:
        message: User's message
        
    Returns:
        AI-generated response
    """
    # You can switch between Gemini and ChatGPT here
    # if USE_OPENAI:
    #     return get_chatgpt_response(message)
    # else:
    return get_gemini_response(message)


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    if "--test" in sys.argv:
        print("\n" + "="*60)
        print("🤖 AI-Powered WhatsApp Chatbot - Test Mode")
        print("="*60)
        
        # Check if API key is set
        if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            print("\n⚠️  WARNING: API Key Not Set!")
            print("\nTo use AI features:")
            print("1. Go to: https://makersuite.google.com/app/apikey")
            print("2. Click 'Create API Key'")
            print("3. Copy the key")
            print("4. Replace 'YOUR_API_KEY_HERE' in this script with your key")
            print("\nRunning test with dummy responses...\n")
        
        test_messages = [
            "Hello! How are you?",
            "What's the weather like today?",
            "Can you help me with Python programming?",
            "Tell me a joke",
            "Thank you!"
        ]
        
        for i, msg in enumerate(test_messages, 1):
            print(f"\n[Test {i}/5]")
            print(f"User: {msg}")
            print("Bot: ", end="", flush=True)
            
            response = generate_ai_response(msg)
            print(response)
            print("-" * 60)
        
        print("\n✅ Test complete!\n")
        
    elif "--interactive" in sys.argv:
        print("\n" + "="*60)
        print("🤖 AI-Powered WhatsApp Chatbot - Interactive Mode")
        print("="*60)
        print("Type your messages and get AI responses.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye!\n")
                    break
                
                if not user_input:
                    continue
                
                print("Bot: ", end="", flush=True)
                response = generate_ai_response(user_input)
                print(response + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
    
    else:
        print("""
🤖 AI-Powered WhatsApp Chatbot
==============================

Usage:
  python whatsapp_ai_chatbot.py --test         Run automated tests
  python whatsapp_ai_chatbot.py --interactive  Chat with the bot

Setup:
1. Get your free Gemini API key: https://makersuite.google.com/app/apikey
2. Replace YOUR_API_KEY_HERE in this script
3. Run the test mode to verify it works

For WhatsApp integration, see README.md
""")
