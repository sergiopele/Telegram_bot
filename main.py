import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)
from Estrans_cargo_bot import (
    start, choose_action, get_name, get_phone,
    get_address, get_message, cancel,
    CHOOSING, NAME, PHONE, ADDRESS, MESSAGE
)

# Bot token and webhook config
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://remarkable-happiness.up.railway.app{WEBHOOK_PATH}"

# Create bot application
application = ApplicationBuilder().token(TOKEN).build()

# Register full conversation flow
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

# Start the webhook server
if __name__ == "__main__":
    print(f"✅ Bot is starting with webhook: {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL
    )