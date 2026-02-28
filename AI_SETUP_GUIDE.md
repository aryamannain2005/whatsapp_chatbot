# AI Setup Guide - Make Your Chatbot Intelligent! 🧠

## Problem
Your chatbot currently uses simple keyword matching ("hello" → "Hello! Welcome..."). 
You want it to use AI like ChatGPT or Gemini to give intelligent, contextual responses.

## Solution: Use Google Gemini AI (FREE!)

### Step 1: Get Your Free Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the API key (it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

💡 **Note:** Gemini API is FREE with generous limits (60 requests per minute)

### Step 2: Test the AI Locally

1. Open the file: `whatsapp_ai_chatbot.py`

2. Find this line (around line 20):
   ```python
   GEMINI_API_KEY = "YOUR_API_KEY_HERE"
   ```

3. Replace `YOUR_API_KEY_HERE` with your actual API key:
   ```python
   GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```

4. Save the file

5. Run the test:
   ```bash
   cd ~/whatsapp_chatbot
   python whatsapp_ai_chatbot.py --test
   ```

6. You should see AI-powered responses! 🎉

### Step 3: Try Interactive Mode

Chat with your AI bot directly:

```bash
python whatsapp_ai_chatbot.py --interactive
```

Type messages and see AI responses in real-time!

## How to Integrate with WhatsApp

### Option A: Update the Python Script

Replace the `generate_response()` function in `whatsapp_chatbot.py`:

```python
# At the top, add:
import requests

GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY"

# Replace the generate_response function with:
def generate_response(message: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""You are a helpful WhatsApp chatbot. Be friendly and concise.
    
    User message: {message}
    
    Respond naturally:"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500}
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        return "Sorry, I'm having trouble right now. Please try again!"
```

### Option B: Use in N8N Workflow

1. Open N8N at `http://localhost:5678`
2. Open your WhatsApp Chatbot workflow
3. Click on the **"Code in Python"** node
4. Replace the code with the content from `ai_chatbot_code.py`
5. Update line 11 with your API key:
   ```python
   GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY"
   ```
6. Save and activate the workflow

### Option C: Use with Node.js Bot

Update `whatsapp_bot.js` to call the AI:

```javascript
const axios = require('axios');

const GEMINI_API_KEY = 'YOUR_ACTUAL_API_KEY';

async function getAIResponse(message) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`;
    
    const payload = {
        contents: [{
            parts: [{
                text: `You are a helpful WhatsApp chatbot. User says: ${message}. Respond naturally:`
            }]
        }]
    };
    
    try {
        const response = await axios.post(url, payload);
        return response.data.candidates[0].content.parts[0].text;
    } catch (error) {
        return "Sorry, I'm having trouble right now!";
    }
}

// In your message handler:
client.on('message', async (message) => {
    const aiResponse = await getAIResponse(message.body);
    await message.reply(aiResponse);
});
```

## Testing Your AI Integration

### Test 1: Simple Greeting
```
User: Hi there!
AI Bot: Hello! 👋 How can I help you today?
```

### Test 2: Question
```
User: What's the capital of France?
AI Bot: The capital of France is Paris! 🇫🇷 It's known for the Eiffel Tower, 
Louvre Museum, and delicious cuisine.
```

### Test 3: Conversation
```
User: Tell me a joke
AI Bot: Why don't scientists trust atoms? 
Because they make up everything! 😄
```

## Troubleshooting

### Error: "API_KEY_INVALID"
- Your API key is wrong or expired
- Get a new one from https://makersuite.google.com/app/apikey

### Error: "403 Forbidden"
- API key doesn't have permission
- Make sure you created it correctly in Google AI Studio

### Error: "429 Too Many Requests"
- You've hit the rate limit (60 requests/minute)
- Wait a minute and try again
- For production, implement rate limiting

### Responses are slow
- AI responses take 1-3 seconds (normal)
- You can add a "typing..." indicator in WhatsApp

### Bot gives generic responses
- Improve your prompt in the code
- Add more context about your business/use case
- Adjust the temperature (0.7 = balanced, 1.0 = creative)

## Alternative: Use ChatGPT Instead

If you prefer OpenAI's ChatGPT:

1. Get API key from: https://platform.openai.com/api-keys
2. Use this code:

```python
import openai

openai.api_key = "YOUR_OPENAI_KEY"

def generate_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful WhatsApp chatbot."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content
```

⚠️ **Note:** ChatGPT is NOT free. It costs ~$0.002 per 1000 tokens.

## Cost Comparison

| Service | Free Tier | Cost After Free Tier |
|---------|-----------|---------------------|
| **Google Gemini** | 60 requests/min | FREE (for now) |
| **OpenAI GPT-3.5** | $5 credit (expires) | $0.002/1K tokens |
| **OpenAI GPT-4** | No free tier | $0.03/1K tokens |

💡 **Recommendation:** Start with Gemini (free), switch to ChatGPT if needed.

## Next Steps

1. ✅ Get Gemini API key
2. ✅ Test with `whatsapp_ai_chatbot.py --test`
3. ✅ Try interactive mode
4. ✅ Integrate with your WhatsApp bot
5. ✅ Customize the AI prompt for your use case
6. ✅ Deploy and enjoy your intelligent chatbot! 🎉

## Need Help?

If you're stuck:
1. Check the error message carefully
2. Verify your API key is correct
3. Make sure you have internet connection
4. Try the test mode first before WhatsApp integration

---

**Happy Coding! 🚀**
