import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)

# Enable logging to Railway
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, NAME, PHONE, ADDRESS, MESSAGE = range(5)
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id] = {}
    keyboard = [[KeyboardButton("Відправити посилку"), KeyboardButton("Купити квиток")]]
    await update.message.reply_text(
        "👋 Вітаємо! Що бажаєте зробити?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    logger.info(f"User {chat_id} started a new session.")
    return CHOOSING

async def choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id]["action"] = update.message.text
    await update.message.reply_text("Введіть ім’я:")
    logger.info(f"User {chat_id} chose action: {update.message.text}")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id]["name"] = update.message.text
    await update.message.reply_text("Введіть номер телефону:")
    logger.info(f"User {chat_id} entered name: {update.message.text}")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id]["phone"] = update.message.text
    await update.message.reply_text("Введіть адресу:")
    logger.info(f"User {chat_id} entered phone: {update.message.text}")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id]["address"] = update.message.text
    await update.message.reply_text("Напишіть повідомлення або деталі:")
    logger.info(f"User {chat_id} entered address: {update.message.text}")
    return MESSAGE

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store[chat_id]["message"] = update.message.text
    data = user_data_store.get(chat_id, {})
    logger.info(f"User {chat_id} completed form: {data}")

    summary = (
        "Дякуємо за заявку!\n\n"
        f"🔹 Дія: {data.get('action')}\n"
        f"👤 Ім’я: {data.get('name')}\n"
        f"📞 Телефон: {data.get('phone')}\n"
        f"📍 Адреса: {data.get('address')}\n"
        f"✉️ Повідомлення: {data.get('message')}\n\n"
        "Наші соцмережі:\n"
        "[Facebook](https://www.facebook.com/profile.php?id=100063475403868)\n"
        "[Telegram](https://t.me/estransuanor)"
    )
    await update.message.reply_text(summary, parse_mode="Markdown")
    return ConversationHandler.END

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_store.pop(chat_id, None)
    logger.info(f"User {chat_id} sent /reset. Session reset.")
    return await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"User {chat_id} cancelled the conversation.")
    await update.message.reply_text("Скасовано.")
    return ConversationHandler.END

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_action)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel), CommandHandler("reset", reset)],
)

app.add_handler(conv_handler)
app.add_handler(CommandHandler("reset", reset))
logger.info("🚀 Estrans Cargo Bot is starting...")
app.run_polling()
