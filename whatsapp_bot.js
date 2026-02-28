// WhatsApp Chatbot using whatsapp-web.js and N8N Integration
// Install dependencies: npm install whatsapp-web.js qrcode-terminal express axios

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

// N8N Webhook URL (update this with your N8N webhook URL)
const N8N_WEBHOOK_URL = 'http://localhost:5678/webhook-test/YOUR_WEBHOOK_ID';

// Initialize WhatsApp client with local authentication
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox']
    }
});

// Generate QR code for authentication
client.on('qr', (qr) => {
    console.log('\n=== Scan this QR code with your WhatsApp ===');
    qrcode.generate(qr, { small: true });
    console.log('\nOpen WhatsApp on your phone > Settings > Linked Devices > Link a Device');
});

// Client ready
client.on('ready', () => {
    console.log('\n✅ WhatsApp Client is ready!');
    console.log('Bot is now listening for messages...\n');
});

// Handle incoming messages
client.on('message', async (message) => {
    console.log(`\n📩 Message from ${message.from}: ${message.body}`);
    
    try {
        // Send message data to N8N webhook
        const response = await axios.post(N8N_WEBHOOK_URL, {
            from: message.from,
            body: message.body,
            timestamp: message.timestamp,
            type: message.type
        });
        
        // Get response from N8N and send back to WhatsApp
        if (response.data && response.data.reply) {
            await message.reply(response.data.reply);
            console.log(`✅ Sent reply: ${response.data.reply}`);
        }
    } catch (error) {
        console.error('❌ Error processing message:', error.message);
        
        // Fallback: Simple chatbot logic if N8N is not available
        const reply = generateSimpleReply(message.body);
        await message.reply(reply);
        console.log(`✅ Sent fallback reply: ${reply}`);
    }
});

// Simple chatbot logic (fallback)
function generateSimpleReply(messageText) {
    const text = messageText.toLowerCase();
    
    if (text.includes('hello') || text.includes('hi') || text.includes('hey')) {
        return '👋 Hello! How can I help you today?';
    } else if (text.includes('help')) {
        return '🤖 I\'m a chatbot. You can ask me anything!\n\nAvailable commands:\n- Say "hello" to greet me\n- Say "help" for this message\n- Say "bye" to end conversation';
    } else if (text.includes('bye') || text.includes('goodbye')) {
        return '👋 Goodbye! Have a great day!';
    } else if (text.includes('thank')) {
        return '😊 You\'re welcome! Happy to help!';
    } else {
        return `I received your message: "${messageText}"\n\nI\'m still learning! Try saying "help" for available commands.`;
    }
}

// Express endpoint to send messages (optional - for testing)
app.post('/send-message', async (req, res) => {
    const { number, message } = req.body;
    
    try {
        const chatId = number.includes('@c.us') ? number : `${number}@c.us`;
        await client.sendMessage(chatId, message);
        res.json({ success: true, message: 'Message sent successfully' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Start Express server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`\n🚀 Express server running on http://localhost:${PORT}`);
    console.log('You can send messages via POST to /send-message\n');
});

// Initialize WhatsApp client
client.initialize();

console.log('\n🔄 Initializing WhatsApp client...');
console.log('Please wait for QR code to appear...\n');
