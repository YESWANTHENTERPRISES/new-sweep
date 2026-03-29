import os
from flask import Flask, request
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace these with your actual bot token and chat ID
TOKEN = "8700179458:AAFLE3KvOsB88h0mQgtumB1uiho86aGlnd4"
CHAT_ID = "8700179458"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    # TradingView sends data in JSON format
    data = request.json
    
    if data:
        # Format the message for Telegram
        ticker = data.get("ticker", "Unknown")
        sweep_type = data.get("type", "Sweep")
        price = data.get("price", "N/A")
        
        msg = f"🚨 *Liquidity Alert* 🚨\n\n*Symbol:* {ticker}\n*Signal:* {sweep_type}\n*Price:* {price}\n*Timeframe:* M5"
        
        send_telegram_message(msg)
        return "Alert Sent", 200
    
    return "No Data", 400

if __name__ == '__main__':
    # Use port 5000 for local testing or environment port for deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)