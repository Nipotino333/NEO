import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

TOKEN = os.getenv("8788750894:AAFojoN5aZt2rTQcymC_Z-LigwYPqXJbW5c")
API_KEY = os.getenv("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")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy NEO, tu asistente personal 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = requests.post(
        "https://api.openrouter.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "minimax/m2.5",
            "messages": [{"role": "user", "content": user_message}]
        }
    )
    reply = response.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

# Aquí agregamos CommandHandler para /start
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
