import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Dispatcher
from flask import Flask, request
import random

# بارگذاری تنظیمات از فایل config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# تنظیمات ربات
TOKEN = config["token"]
ADMIN_IDS = config["admin_ids"]
CHANNEL_ID = config["channel_id"]
WEBHOOK_URL = f"https://{config['domain']}/{TOKEN}"

# لیست واکنش‌ها
reactions = ['❤️', '😆', '😢', '🔥', '👍', '🎉', '😂', '😎', '😜', '😍']

# ذخیره پست مشخص شده توسط ادمین
admin_selected_post = None

# تنظیمات Flask برای Webhook
app = Flask(__name__)

# تابع برای دکمه واکنش دادن به پست‌ها
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in ADMIN_IDS:
        # دکمه برای ادمین
        keyboard = [[InlineKeyboardButton("ارسال 10 واکنش به پست", callback_data='send_reactions')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("سلام ادمین عزیز، برای ارسال واکنش‌ها به پست، دکمه زیر را فشار دهید.", reply_markup=reply_markup)
    else:
        update.message.reply_text("سلام! شما دسترسی به این دکمه را ندارید.")

# تابع برای ارسال 10 واکنش به پست
def send_reactions(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    if user_id in ADMIN_IDS:
        global admin_selected_post
        if admin_selected_post:
            # ارسال 10 واکنش به پست انتخابی ادمین
            for _ in range(10):
                reaction = random.choice(reactions)
                context.bot.send_message(chat_id=admin_selected_post['chat_id'], text=reaction, reply_to_message_id=admin_selected_post['message_id'])
            query.edit_message_text("10 واکنش به پست انتخابی ارسال شد!")
        else:
            query.edit_message_text("پستی انتخاب نشده است. لطفاً یک پست ارسال کنید.")
    else:
        query.edit_message_text("شما دسترسی به این عملیات را ندارید.")

# تابع برای ذخیره پست انتخابی ادمین
def save_post(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in ADMIN_IDS:
        global admin_selected_post
        admin_selected_post = {
            'chat_id': update.message.chat.id,
            'message_id': update.message.message_id
        }
        update.message.reply_text("پست شما برای ارسال واکنش‌ها انتخاب شد!")
    else:
        update.message.reply_text("شما دسترسی به این عملیات را ندارید.")

# تابع برای دریافت آپدیت‌ها از Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return 'OK', 200

# تابع اصلی ربات
def main():
    # ایجاد اپدیت و اپراتور
    global dp
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, save_post))  # برای ذخیره پست ادمین
    dp.add_handler(CallbackQueryHandler(send_reactions, pattern='send_reactions'))

    # تنظیم Webhook
    bot.set_webhook(url=WEBHOOK_URL)

    # شروع اپلیکیشن Flask
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    main()
