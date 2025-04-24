import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)
from Estrans_cargo_bot import (
    start, choose_action, get_name, get_phone,
    get_address, get_message, cancel,
    CHOOSING, NAME, PHONE, ADDRESS, MESSAGE
)

# Load token
TOKEN = os.getenv("BOT_TOKEN")

# Initialize Flask
app = Flask(__name__)

# Build telegram bot app
application = ApplicationBuilder().token(TOKEN).build()

# Handlers
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_action)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(conv_handler)

# Run as webhook listener
if __name__ == "__main__":
    # 🚨 Launch webhook server (built-in to PTB) instead of Flask
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"https://remarkable-happiness.up.railway.app/{TOKEN}"
    )