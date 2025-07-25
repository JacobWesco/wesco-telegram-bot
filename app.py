from flask import Flask, request
import os
import requests

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route('/')
def index():
    return "Bot działa."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or 'message' not in data:
        return 'No message', 200

    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    if text == '/tablica':
        # przykładowa odpowiedź – tu możesz połączyć z Google Sheets API
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
            "chat_id": chat_id,
            "text": "📊 Dane z arkusza (tu podłączysz Google Sheets)"
        })

    return 'OK', 200
