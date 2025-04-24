import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from Estrans_cargo_bot import start  # Ensure this exists and is a handler

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Register handlers
application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/", methods=["GET"])
def health():
    return "Bot is running."

if __name__ == "__main__":
    app.run(port=5000)
