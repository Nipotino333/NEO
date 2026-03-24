import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy NEO, tu asistente personal 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = requests.post(
            "https://api.openrouter.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "minimax/m2.7",
                "messages": [{"role": "user", "content": user_message}]
            },
            timeout=30  # clave para no colgar si tarda mucho
        )
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "Ups, hubo un error. Intenta de nuevo."
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
