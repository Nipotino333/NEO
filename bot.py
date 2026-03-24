import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import logging
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

def request_openrouter(user_message: str) -> str:
    payload = {
        "model": "minimax/m2.5",
        "messages": [{"role": "user", "content": user_message}]
    }
    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.openrouter.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Intento {attempt+1} - Error en OpenRouter:", e)
            time.sleep(2)
    return "Ups, la IA no responde ahora. Intenta de nuevo."

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hola! Soy NEO, tu asistente personal 🤖")

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    reply = request_openrouter(user_message)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import logging
import time

# Activa logging para ver errores en Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variables de entorno
TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

# Función para enviar petición a OpenRouter con reintentos
def request_openrouter(user_message: str) -> str:
    payload = {
        "model": "minimax/m2.5",  # Cambia si quieres otro modelo
        "messages": [{"role": "user", "content": user_message}]
    }
    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.openrouter.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Intento {attempt+1} - Error en OpenRouter:", e)
            time.sleep(2)
    return "Ups, la IA no responde ahora. Intenta de nuevo."

# /start handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hola! Soy NEO, tu asistente personal 🤖")

# Mensajes normales
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    reply = request_openrouter(user_message)
    await update.message.reply_text(reply)

# Inicia el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run webhook (más estable en la nube)
    # Cambia el URL a tu dominio Railway si quieres usar webhook
    # app.run_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 8443)), webhook_url="https://tuapp.up.railway.app/" + TOKEN)

    # Para empezar rápido con polling (funciona pero puede dar conflicto si hay otra sesión)
    app.run_polling()
