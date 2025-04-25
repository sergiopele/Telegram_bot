import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and responding!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return "ok"

@app.route("/", methods=["GET"])
def health():
    return "✅ Bot is running."

if __name__ == "__main__":
    print("🚀 Flask bot starting on Railway...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))