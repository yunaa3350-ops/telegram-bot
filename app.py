import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

PRODUCTS = [
    {"name": "CAPCUT PRIVATE", "stok": 145},
    {"name": "V1D10 PRIV PLATNM", "stok": 52},
    {"name": "APPLE MUSIC", "stok": 0},
    {"name": "CANVA", "stok": 0},
    {"name": "CHAT GPT", "stok": 0},
    {"name": "DISNEY SHAR 5U", "stok": 0},
    {"name": "GROK", "stok": 0},
    {"name": "HBO MAX PRIVATE", "stok": 0},
    {"name": "IQIYI REG INDONESIA", "stok": 0},
    {"name": "IQIYI REG HONGKONG", "stok": 0},
]

def main_menu():
    text = "✨ KATALOG PRODUK UTAMA ✨\n\n"
    buttons = []
    row = []
    for i, p in enumerate(PRODUCTS):
        text += f"{i+1}. {p['name']} (Stok: {p['stok']})\n"
        row.append(InlineKeyboardButton(str(i+1), callback_data=str(i)))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return text, InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, kb = main_menu()
    await update.message.reply_text(text, reply_markup=kb)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data)
    product = PRODUCTS[index]
    await query.edit_message_text(
        f"📦 {product['name']}\nStok: {product['stok']}"
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    application.run_polling()
