#!/usr/bin/env python3
"""
WhatsApp Chatbot with Python and N8N
=====================================
This script provides a standalone WhatsApp chatbot implementation
that can be used alongside the N8N workflow.

Author: Created with Vy Assistant
Date: February 28, 2026
"""

import requests
import json
from typing import Optional, Dict, Any

# =============================================================================
# CONFIGURATION - Replace these with your actual values
# =============================================================================

WHATSAPP_CONFIG = {
    "phone_number_id": "YOUR_PHONE_NUMBER_ID",  # From Meta Developer Console
    "access_token": "YOUR_ACCESS_TOKEN",         # From Meta Developer Console
    "api_version": "v17.0",
    "verify_token": "your_custom_verify_token"   # For webhook verification
}

# =============================================================================
# CHATBOT RESPONSES
# =============================================================================

RESPONSES = {
    "greetings": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
    "help": ["help", "support", "assist", "how", "what can you do"],
    "thanks": ["thank", "thanks", "appreciate"],
    "goodbye": ["bye", "goodbye", "see you", "later"]
}

RESPONSE_MESSAGES = {
    "greetings": "Hello! 👋 Welcome to our WhatsApp Chatbot. How can I help you today?",
    "help": "I can help you with:\n• General inquiries\n• Product information\n• Support requests\n\nJust type your question!",
    "thanks": "You're welcome! 😊 Is there anything else I can help you with?",
    "goodbye": "Goodbye! 👋 Have a great day! Feel free to message us anytime.",
    "default": "Thanks for your message! I'm a simple chatbot. Type 'help' to see what I can do."
}

# =============================================================================
# CHATBOT LOGIC
# =============================================================================

def generate_response(message: str) -> str:
    """
    Generate a response based on the incoming message.
    
    Args:
        message: The incoming message text
        
    Returns:
        The chatbot response string
    """
    message_lower = message.lower().strip()
    
    # Check for greetings
    for keyword in RESPONSES["greetings"]:
        if keyword in message_lower:
            return RESPONSE_MESSAGES["greetings"]
    
    # Check for help requests
    for keyword in RESPONSES["help"]:
        if keyword in message_lower:
            return RESPONSE_MESSAGES["help"]
    
    # Check for thanks
    for keyword in RESPONSES["thanks"]:
        if keyword in message_lower:
            return RESPONSE_MESSAGES["thanks"]
    
    # Check for goodbye
    for keyword in RESPONSES["goodbye"]:
        if keyword in message_lower:
            return RESPONSE_MESSAGES["goodbye"]
    
    # Default response
    return RESPONSE_MESSAGES["default"]


def send_whatsapp_message(to: str, message: str) -> Dict[str, Any]:
    """
    Send a WhatsApp message using the Cloud API.
    
    Args:
        to: The recipient's phone number (with country code, no + sign)
        message: The message text to send
        
    Returns:
        The API response as a dictionary
    """
    url = f"https://graph.facebook.com/{WHATSAPP_CONFIG['api_version']}/{WHATSAPP_CONFIG['phone_number_id']}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['access_token']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def parse_webhook_payload(payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Parse the incoming webhook payload from WhatsApp.
    
    Args:
        payload: The webhook payload dictionary
        
    Returns:
        Dictionary with 'from' and 'message' keys, or None if invalid
    """
    try:
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if messages:
            message = messages[0]
            return {
                "from": message.get("from", ""),
                "message": message.get("text", {}).get("body", "")
            }
    except (IndexError, KeyError, TypeError):
        pass
    
    return None


def handle_incoming_message(payload: Dict[str, Any]) -> Optional[str]:
    """
    Handle an incoming WhatsApp message and send a response.
    
    Args:
        payload: The webhook payload from WhatsApp
        
    Returns:
        The response message sent, or None if no message was processed
    """
    parsed = parse_webhook_payload(payload)
    
    if parsed and parsed["message"]:
        response = generate_response(parsed["message"])
        send_whatsapp_message(parsed["from"], response)
        return response
    
    return None


# =============================================================================
# FLASK SERVER (Optional - for standalone use without N8N)
# =============================================================================

def create_flask_app():
    """
    Create a Flask app for handling webhooks directly (without N8N).
    
    To use this, install Flask: pip install flask
    Then run: python whatsapp_chatbot.py --server
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Flask not installed. Run: pip install flask")
        return None
    
    app = Flask(__name__)
    
    @app.route("/webhook", methods=["GET"])
    def verify_webhook():
        """Verify the webhook with Meta."""
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == WHATSAPP_CONFIG["verify_token"]:
            return challenge, 200
        return "Forbidden", 403
    
    @app.route("/webhook", methods=["POST"])
    def handle_webhook():
        """Handle incoming webhook messages."""
        payload = request.get_json()
        handle_incoming_message(payload)
        return jsonify({"status": "ok"}), 200
    
    return app


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if "--server" in sys.argv:
        # Run as standalone Flask server
        app = create_flask_app()
        if app:
            print("Starting WhatsApp Chatbot Server...")
            print("Webhook URL: http://localhost:5000/webhook")
            app.run(host="0.0.0.0", port=5000, debug=True)
    elif "--test" in sys.argv:
        # Test the chatbot responses
        test_messages = [
            "Hello!",
            "Can you help me?",
            "Thank you so much!",
            "Goodbye!",
            "What's the weather like?"
        ]
        
        print("Testing Chatbot Responses:")
        print("=" * 50)
        for msg in test_messages:
            response = generate_response(msg)
            print(f"\nUser: {msg}")
            print(f"Bot: {response}")
    else:
        print("""
WhatsApp Chatbot with Python and N8N
=====================================

Usage:
  python whatsapp_chatbot.py --test     Test chatbot responses
  python whatsapp_chatbot.py --server   Run standalone Flask server

For N8N integration, this script's logic is already embedded in the
N8N workflow's 'Code in Python' node.

See README.md for complete setup instructions.
""")
