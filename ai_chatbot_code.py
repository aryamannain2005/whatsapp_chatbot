# AI-Powered WhatsApp Chatbot Code for N8N
# This code uses Google Gemini API (free) to generate intelligent responses
# Copy this code into your N8N "Code in Python" node

import json
import requests

# ============================================
# CONFIGURATION - Add your API key here
# ============================================
GEMINI_API_KEY = "AIzaSyCP1HNCANX6VBIHGGGNiKyQsjqtryqypfI"  # Get free key from: https://makersuite.google.com/app/apikey

# ============================================
# MAIN CHATBOT LOGIC
# ============================================

def get_ai_response(user_message):
    """
    Sends message to Google Gemini AI and gets intelligent response
    Automatically detects language and responds in the same language
    """
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    
    # System prompt to make the bot friendly and multilingual
    prompt = f"""You are a helpful and friendly WhatsApp chatbot assistant. 
    
Rules:
1. Detect the language of the user's message and respond in THE SAME LANGUAGE
2. Be conversational, warm, and helpful
3. Keep responses concise (2-3 sentences max for casual chat)
4. If user asks questions, provide helpful answers
5. Match the user's tone and style

User message: {user_message}

Respond naturally in the same language as the user's message."""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        ai_response = data['candidates'][0]['content']['parts'][0]['text']
        return ai_response.strip()
        
    except Exception as e:
        # Fallback response if AI fails
        return "Sorry, I'm having trouble processing your message right now. Please try again!"


# ============================================
# N8N INTEGRATION CODE
# ============================================

# Get incoming webhook data
webhook_data = items[0].json

# Extract message and sender from WhatsApp webhook
try:
    # WhatsApp Cloud API format
    entry = webhook_data.get('entry', [{}])[0]
    changes = entry.get('changes', [{}])[0]
    value = changes.get('value', {})
    messages = value.get('messages', [{}])
    
    if messages:
        message_data = messages[0]
        sender_phone = message_data.get('from', '')
        message_text = message_data.get('text', {}).get('body', '')
    else:
        # Fallback for test messages
        sender_phone = webhook_data.get('from', 'unknown')
        message_text = webhook_data.get('text', webhook_data.get('message', ''))
        
except Exception as e:
    # Simple format fallback
    sender_phone = webhook_data.get('from', 'unknown')
    message_text = webhook_data.get('text', webhook_data.get('message', 'hello'))

# Get AI-powered response
ai_response = get_ai_response(message_text)

# Return data for next node (HTTP Request)
return {
    'response': ai_response,
    'sender': sender_phone,
    'original_message': message_text
}
