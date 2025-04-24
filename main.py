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

# Load token from Railway environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Initialize Flask and Bot
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Build Telegram application
application = ApplicationBuilder().token(TOKEN).build()

# Register the full conversation flow
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

# Initialize app so it starts processing updates via webhook
application.initialize()

# Define the webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

# Health check
@app.route("/", methods=["GET"])
def health():
    return "🚀 Telegram Bot is running."

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))