import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN not set!")

app = Flask(__name__)

# Global Telegram application
telegram_app = Application.builder().token(TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and responding!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.create_task(telegram_app.process_update(update))  # <-- correct method
    return "ok", 200

@app.route("/", methods=["GET"])
def health():
    return "✅ Flask bot is running."

if __name__ == "__main__":
    print("🚀 Flask bot starting on Railway...")
    telegram_app.initialize()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))