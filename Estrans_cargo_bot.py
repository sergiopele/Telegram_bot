from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

CHOOSING, NAME, PHONE, ADDRESS, MESSAGE = range(5)

YOUR_ID = 535744015

SOCIAL_LINKS = (
    "Дякуємо за заявку!\n\nНаші соцмережі:\n"
    "<a href='https://www.facebook.com/groups/1814614405457006?locale=uk_UA'>Facebook</a>\n"
    "<a href='https://t.me/estransuanor'>Telegram</a>"
)

CONTACT_LINKS = (
    "Контакти водія:\n"
    "WhatsApp: https://wa.me/380963508202\n"
    "Telegram: https://t.me/Phant0mWAdeR\n"
    "Телефон: +4796801527"
)

PRICING_URL = "https://t.me/estransuanor/13"

MAIN_MENU = ReplyKeyboardMarkup(
    [["Оформити заявку"], ["Зв’язок з водієм", "Умови та розцінки"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start command received")
    await update.message.reply_text("Привіт! Обери дію:", reply_markup=MAIN_MENU)
    return CHOOSING

async def choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Оформити заявку":
        await update.message.reply_text("Введіть своє ім’я:")
        return NAME
    elif text == "Зв’язок з водієм":
        await update.message.reply_text(CONTACT_LINKS)
    elif text == "Умови та розцінки":
        await update.message.reply_text(f"Ознайомтеся з умовами:\n{PRICING_URL}")

    await update.message.reply_text("Обери наступну дію:", reply_markup=MAIN_MENU)
    return CHOOSING

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введіть номер телефону:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Введіть адресу (місто, вулиця, номер):")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("Напишіть повідомлення або деталі:")
    return MESSAGE

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['message'] = update.message.text
    summary = (
        f"Нова заявка:\n"
        f"Ім’я: {context.user_data['name']}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Адреса: {context.user_data['address']}\n"
        f"Повідомлення: {context.user_data['message']}"
    )
    await context.bot.send_message(chat_id=YOUR_ID, text=summary)
    await update.message.reply_text(SOCIAL_LINKS, parse_mode="HTML")
    await update.message.reply_text("Готово! Оберіть наступну дію:", reply_markup=MAIN_MENU)
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Скасовано.", reply_markup=MAIN_MENU)
    return CHOOSING