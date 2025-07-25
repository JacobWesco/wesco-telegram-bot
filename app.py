
from flask import Flask, request
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# --- konfiguracja Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1lIehR7HSct4bpoj1v0L6W-1lAMh2b0z1oCDm5JPt5bo").sheet1
data = sheet.get_all_values()

# --- pomocnicza funkcja do wysyłki wiadomości ---
def send_telegram_message(chat_id, text):
    TOKEN = "TELEGRAM_TOKEN"  # Podmień na nazwę zmiennej środowiskowej jeśli chcesz
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# --- wyszukiwanie kierowcy po imieniu/nazwisku ---
def znajdz_wiersz(kryterium):
    kryterium = kryterium.lower().strip()
    for row in data[1:]:
        imie_nazwisko = row[0].lower()
        if kryterium in imie_nazwisko:
            return row
    return None

# --- obsługa webhooka ---
@app.route("/webhook", methods=["POST"])
def webhook():
    dane = request.get_json()
    chat_id = dane["message"]["chat"]["id"]
    tekst = dane["message"].get("text", "")
    czesci = tekst.strip().split(" ", 1)

    if len(czesci) < 2:
        send_telegram_message(chat_id, "❗ Podaj też nazwisko lub imię i nazwisko kierowcy.")
        return "OK"

    komenda, argument = czesci[0], czesci[1]
    wiersz = znajdz_wiersz(argument)

    if not wiersz:
        send_telegram_message(chat_id, "❌ Kierowca nie znaleziony.")
        return "OK"

    if komenda == "/link":
        send_telegram_message(chat_id, f"🔗 Link: {wiersz[4]}")
    elif komenda == "/dane":
        send_telegram_message(chat_id, f"📄 Dane: {wiersz[0]} | {wiersz[1]} | {wiersz[2]}")
    elif komenda == "/amazon":
        send_telegram_message(chat_id, f"📦 Amazon: {wiersz[1]} | {wiersz[2]}")
    else:
        send_telegram_message(chat_id, "❓ Nieznana komenda.")

    return "OK"
