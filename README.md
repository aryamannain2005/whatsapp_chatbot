# WhatsApp Chatbot with Python and N8N

A complete WhatsApp chatbot solution using Python for logic and N8N for workflow automation.

## 📌 Overview

This project creates a WhatsApp chatbot that:
- Receives messages via WhatsApp Business API
- Processes messages using Python logic
- Sends automated responses back to users

## 🛠️ Components

1. **N8N Workflow** - Handles webhook reception and API calls
2. **Python Script** - Contains chatbot logic and responses
3. **WhatsApp Business API** - Connects to WhatsApp

---

## 🚀 Setup Instructions

### Step 1: N8N Setup (Already Complete)

N8N is installed and running at: `http://localhost:5678`

The workflow "WhatsApp Chatbot" contains:
- **Webhook Node**: Receives incoming messages (POST)
- **Code in Python Node**: Processes messages and generates responses
- **HTTP Request Node**: Sends responses via WhatsApp API

### Step 2: WhatsApp Business API Setup

#### 2.1 Create Meta Developer Account

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click "Get Started" or "Log In"
3. Create a developer account if you don't have one

#### 2.2 Create a Meta App

1. Go to [Meta Apps Dashboard](https://developers.facebook.com/apps/)
2. Click "Create App"
3. Select "Business" as the app type
4. Fill in:
   - App name: "WhatsApp Chatbot"
   - Contact email: Your email
5. Click "Create App"

#### 2.3 Add WhatsApp Product

1. In your app dashboard, find "Add Products"
2. Find "WhatsApp" and click "Set Up"
3. Follow the prompts to set up WhatsApp Business

#### 2.4 Get API Credentials

1. In the WhatsApp section, go to "API Setup"
2. Note down:
   - **Phone Number ID**: Found under "From" phone number
   - **WhatsApp Business Account ID**
   - **Temporary Access Token**: Click "Generate" (valid for 24 hours)

   For permanent token:
   1. Go to Business Settings > System Users
   2. Create a system user
   3. Generate a permanent access token with `whatsapp_business_messaging` permission

#### 2.5 Configure Webhook in Meta

1. In WhatsApp > Configuration, find "Webhook"
2. Click "Edit"
3. Enter:
   - **Callback URL**: Your N8N webhook URL (needs to be publicly accessible)
   - **Verify Token**: A custom string you create (e.g., "my_verify_token_123")
4. Click "Verify and Save"
5. Subscribe to "messages" webhook field

> ⚠️ **Important**: For local development, you need to expose your N8N webhook using a tool like [ngrok](https://ngrok.com/):
> ```bash
> ngrok http 5678
> ```
> Then use the ngrok URL as your callback URL.

### Step 3: Update N8N Workflow

1. Open N8N at `http://localhost:5678`
2. Open the "WhatsApp Chatbot" workflow
3. Click on the "HTTP Request" node
4. Update the URL with your Phone Number ID:
   ```
   https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages
   ```
5. Update the Authorization header with your access token:
   ```
   Bearer YOUR_ACCESS_TOKEN
   ```
6. Save the workflow
7. Click "Publish" to activate the workflow

### Step 4: Test the Chatbot

#### Using Meta's Test Number

1. In Meta Developer Console > WhatsApp > API Setup
2. Find "Send and receive messages"
3. Add your phone number to receive test messages
4. Send a message to the test number
5. Check N8N executions to see the workflow run

#### Using the Python Script

```bash
# Test chatbot responses locally
python whatsapp_chatbot.py --test
```

---

## 📁 Project Files

```
whatsapp_chatbot/
├── README.md              # This file
├── whatsapp_chatbot.py    # Python chatbot script
└── requirements.txt       # Python dependencies
```

---

## 🔧 Configuration

### Environment Variables (Optional)

For production, use environment variables instead of hardcoding:

```bash
export WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id"
export WHATSAPP_ACCESS_TOKEN="your_access_token"
export WHATSAPP_VERIFY_TOKEN="your_verify_token"
```

### N8N Credentials

N8N login credentials:
- URL: http://localhost:5678
- Email: aryamannain2005@gmail.com
- Password: N8nChatbot2026!

---

## 💬 Customizing Responses

### In N8N (Code in Python Node)

Edit the `responses` dictionary in the Code node:

```python
responses = {
    "greetings": "Your custom greeting message",
    "help": "Your custom help message",
    "thanks": "Your custom thanks message",
    "goodbye": "Your custom goodbye message",
    "default": "Your default response"
}
```

### In Python Script

Edit `RESPONSE_MESSAGES` in `whatsapp_chatbot.py`:

```python
RESPONSE_MESSAGES = {
    "greetings": "Hello! Welcome to our service!",
    "help": "Here's how I can help...",
    # ... add more
}
```

---

## 🚨 Troubleshooting

### N8N Issues

**N8N won't start:**
```bash
# Check if port 5678 is in use
lsof -i :5678

# Start with secure cookie disabled (for local dev)
N8N_SECURE_COOKIE=false n8n start
```

**Webhook not receiving messages:**
1. Ensure workflow is published/activated
2. Check the webhook URL is publicly accessible
3. Verify the webhook is subscribed to "messages" in Meta Console

### WhatsApp API Issues

**401 Unauthorized:**
- Access token expired (regenerate in Meta Console)
- Token doesn't have correct permissions

**400 Bad Request:**
- Check phone number format (include country code, no + sign)
- Verify JSON payload structure

**Recipient not in allowed list:**
- In test mode, add recipient's number to allowed list in Meta Console

---

## 📚 Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [N8N Documentation](https://docs.n8n.io/)
- [Meta for Developers](https://developers.facebook.com/)
- [ngrok](https://ngrok.com/) - For exposing local webhooks

---

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with WhatsApp's Terms of Service.

---

Created with ❤️ using Vy Assistant | February 28, 2026
