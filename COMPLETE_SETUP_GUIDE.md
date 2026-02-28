# Complete WhatsApp Chatbot Setup Guide
## Using Python, N8N, and whatsapp-web.js

---

## 🎯 What You've Built

A complete WhatsApp chatbot system with:
1. **N8N Workflow** - Visual automation platform for message processing
2. **Python Chatbot Logic** - Smart responses based on keywords
3. **WhatsApp Integration** - Using whatsapp-web.js (no Meta Business API needed!)

---

## 📁 Project Structure

```
~/whatsapp_chatbot/
├── whatsapp_bot.js          # Main WhatsApp bot (Node.js)
├── whatsapp_chatbot.py      # Python chatbot logic
├── package.json             # Node.js dependencies
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
├── SETUP_GUIDE.md          # Meta API setup (alternative)
└── COMPLETE_SETUP_GUIDE.md # This file
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Fix NPM Permissions (Required)

The npm install failed due to permission issues. Fix it:

```bash
cd ~/whatsapp_chatbot

# Option A: Fix permissions (recommended)
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) ~/whatsapp_chatbot

# Option B: Use a different npm prefix
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
```

### Step 2: Install Dependencies

```bash
# Install Node.js packages
npm install whatsapp-web.js qrcode-terminal express axios --legacy-peer-deps

# Install Python packages (optional)
pip3 install flask requests
```

### Step 3: Start the Bot

```bash
# Terminal 1: Start N8N (if not already running)
n8n

# Terminal 2: Start WhatsApp Bot
node whatsapp_bot.js
```

A QR code will appear - scan it with WhatsApp on your phone!

---

## 🔧 Configuration

### Update N8N Webhook URL

Edit `whatsapp_bot.js` line 11:

```javascript
const N8N_WEBHOOK_URL = 'http://localhost:5678/webhook-test/YOUR_WEBHOOK_ID';
```

Get your webhook ID from N8N:
1. Open N8N: http://localhost:5678
2. Open "WhatsApp Chatbot" workflow
3. Click on Webhook node
4. Copy the webhook URL
5. Replace YOUR_WEBHOOK_ID in whatsapp_bot.js

### N8N Workflow Configuration

Your N8N workflow is already set up with:

**1. Webhook Node (Trigger)**
- Method: POST
- Path: webhook-test/...
- Receives: WhatsApp message data

**2. Code in Python Node**
- Parses incoming message
- Generates smart responses
- Returns reply text

**3. HTTP Request Node (Optional)**
- For Meta WhatsApp API integration
- Not needed for whatsapp-web.js approach

---

## 📱 How It Works

```
┌─────────────┐
│  WhatsApp   │
│   Message   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ whatsapp_bot.js │  ← Receives message
│  (Node.js)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   N8N Webhook   │  ← Processes with Python
│  (localhost)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Python Chatbot  │  ← Generates response
│     Logic       │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   WhatsApp      │  ← Sends reply
│    Reply        │
└─────────────────┘
```

---

## 🧪 Testing

### Test 1: Direct Bot (No N8N)

1. Start the bot: `node whatsapp_bot.js`
2. Scan QR code with WhatsApp
3. Send a message to your own number
4. Bot will reply with fallback responses

### Test 2: With N8N Integration

1. Make sure N8N is running
2. Update webhook URL in whatsapp_bot.js
3. Start the bot
4. Send messages - they'll be processed by N8N

### Test 3: Send Message via API

```bash
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "number": "1234567890",
    "message": "Hello from API!"
  }'
```

---

## 🎨 Customizing Responses

### Option 1: Edit whatsapp_bot.js

Modify the `generateSimpleReply()` function:

```javascript
function generateSimpleReply(messageText) {
    const text = messageText.toLowerCase();
    
    // Add your custom responses here
    if (text.includes('price')) {
        return '💰 Our prices start at $10. Visit our website for details!';
    }
    // ... more conditions
}
```

### Option 2: Edit N8N Python Node

In N8N workflow > Code in Python node:

```python
# Add more keyword responses
if 'order' in message_text:
    response = "📦 To place an order, visit our website or call us!"
elif 'hours' in message_text:
    response = "🕐 We're open Mon-Fri 9AM-5PM"
```

---

## 🐛 Troubleshooting

### Issue: QR Code Not Appearing

**Solution:**
```bash
# Clear authentication data
rm -rf ~/.wwebjs_auth
node whatsapp_bot.js
```

### Issue: "Cannot find module 'whatsapp-web.js'"

**Solution:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install whatsapp-web.js qrcode-terminal express axios --legacy-peer-deps
```

### Issue: N8N Webhook Not Responding

**Solution:**
1. Check N8N is running: http://localhost:5678
2. Verify webhook URL in whatsapp_bot.js
3. Check N8N workflow is activated (toggle switch)

### Issue: Bot Disconnects Frequently

**Solution:**
```javascript
// Add to whatsapp_bot.js
client.on('disconnected', (reason) => {
    console.log('Client was logged out', reason);
    client.initialize();
});
```

---

## 🔐 Security Notes

1. **Never share your QR code** - It gives full access to your WhatsApp
2. **Use environment variables** for sensitive data:
   ```bash
   export N8N_WEBHOOK_URL="your_webhook_url"
   ```
3. **Add rate limiting** to prevent spam
4. **Validate incoming messages** before processing

---

## 🚀 Next Steps

### 1. Add Database Storage
```bash
npm install sqlite3
# Store conversation history
```

### 2. Add AI Integration
```bash
npm install openai
# Use ChatGPT for responses
```

### 3. Add Media Support
```javascript
client.on('message', async (message) => {
    if (message.hasMedia) {
        const media = await message.downloadMedia();
        // Process images, videos, etc.
    }
});
```

### 4. Deploy to Server
```bash
# Use PM2 for production
npm install -g pm2
pm2 start whatsapp_bot.js
pm2 startup
pm2 save
```

---

## 📚 Resources

- **whatsapp-web.js Docs**: https://wwebjs.dev/
- **N8N Documentation**: https://docs.n8n.io/
- **Node.js Guide**: https://nodejs.org/en/docs/
- **Python Flask**: https://flask.palletsprojects.com/

---

## ✅ What's Already Done

✅ N8N installed and running (v2.8.4)
✅ N8N workflow created ("WhatsApp Chatbot")
✅ Webhook node configured
✅ Python chatbot logic implemented
✅ Project structure created
✅ Documentation written

## ⏳ What You Need to Do

1. Fix npm permissions (see Step 1 above)
2. Install Node.js dependencies
3. Update webhook URL in whatsapp_bot.js
4. Run the bot and scan QR code
5. Test with WhatsApp messages

---

## 💡 Tips

- Keep N8N running in one terminal
- Keep the bot running in another terminal
- Use `pm2` for production deployment
- Test thoroughly before going live
- Monitor logs for errors

---

## 🎉 Success!

Once everything is running, you'll have a fully functional WhatsApp chatbot that:
- ✅ Responds to messages automatically
- ✅ Processes messages through N8N
- ✅ Uses Python for smart responses
- ✅ Works without Meta Business API
- ✅ Can be customized easily

Happy chatting! 🤖💬
