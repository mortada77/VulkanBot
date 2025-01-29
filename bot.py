from telegram import Update, Bot
from telegram.ext import CommandHandler, Dispatcher
import requests
from flask import Flask, request

# 🔥 توكن البوت الخاص بك
TOKEN = "7696945696:AAFY140rEeI-yRCNURRhmIXNXL79iD1xE4Q"

# 🔥 سيتم استبدال هذا بالرابط النهائي بعد نشر البوت على Render
WEBHOOK_URL = "https://YOUR_RENDER_APP_URL/webhook"

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

def start(update: Update, context) -> None:
    update.message.reply_text("🚀 أهلاً بك في ڤُلكان! جاهز لتحليل العملات الرقمية.")

def price(update: Update, context) -> None:
    if not context.args:
        update.message.reply_text("💰 استخدم الأمر بالشكل التالي:\n`/price BTC` أو `/price ETH`")
        return
    
    coin = context.args[0].upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        price = response.json()["price"]
        update.message.reply_text(f"💰 سعر {coin}: {price} USDT")
    else:
        update.message.reply_text(f"⚠️ لم أتمكن من جلب سعر {coin}. تأكد من صحة الرمز.")

if __name__ == '__main__':
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", price))

    app.run(host="0.0.0.0", port=8080)
