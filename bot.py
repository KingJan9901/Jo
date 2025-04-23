from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import json
import config

# بارگذاری داده‌ها
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "words": []}

# ذخیره داده‌ها
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

data = load_data()

# شروع
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"سلام {user.first_name}! خوش اومدی.")

# پاسخ به پیام‌ها
async def reply_text(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if text == "سلام":
        await update.message.reply_text("سلام عزیزم!")
    elif text == "چطوری":
        await update.message.reply_text("من خوبم، تو چطوری؟")
    else:
        await update.message.reply_text("متوجه نشدم چی گفتی.")

def main():
    app = Application.builder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

    print("ربات فعال است...")
    app.run_polling()

if __name__ == "__main__":
    main()
