
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN bota z @BotFather (Wstaw swój własny)
TELEGRAM_TOKEN = "7406178231:AAEw02WVvH__d-riVF5OmHulZA6U--ZAeWI"
# Link do Twojego Web Appa Google Apps Script
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxE4Eu-DeP_EYDrCRGcvHgPJqQs5gVT_zNts-2gyqYmdNiwL0lYUaS35h66j79DaH1ZCg/exec"

# Komenda /kierowca Imie Nazwisko
async def kierowca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Wpisz imię i nazwisko kierowcy, np. /kierowca Piotr Jangas")
        return

    imie_nazwisko = " ".join(context.args)
    try:
        response = requests.post(
            WEBAPP_URL,
            json={"kierowca": imie_nazwisko},
            timeout=10
        )
        if response.status_code == 200:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("❌ Błąd połączenia z arkuszem.")
    except Exception as e:
        await update.message.reply_text(f"❌ Wyjątek: {str(e)}")

# Start
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("kierowca", kierowca))
    print("✅ Bot uruchomiony.")
    app.run_polling()
