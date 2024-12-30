from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
import re
from currency_converter import CurrencyConverter
from settings import *
import os
from dotenv import load_dotenv

load_dotenv()

cur_api = os.getenv("TOKEN_CURRENCY")
converter = CurrencyConverter(cur_api)

selected_language = 'en'

async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='en'),
            InlineKeyboardButton("Russian", callback_data='ru'),
            InlineKeyboardButton("Ukranian", callback_data='ua'),
            InlineKeyboardButton("Czech", callback_data='cz')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Please choose:", reply_markup=reply_markup)



async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_language
    query = update.callback_query
    await query.answer()

    selected_language = query.data  #either ru en cz
    await query.edit_message_text(languages[selected_language]['selected'])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_language
    await update.message.reply_text(languages[selected_language]["help"], parse_mode='Markdown')



async def base(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_language
    users_text = update.message.text
    pattern = r'(\d+)\s*([A-Za-z]+)|([A-Za-z]+)\s*(\d+)'
    match = re.search(pattern, users_text)

    if match:
        if match.group(1):
            amount = match.group(1)
            base_currency = match.group(2).upper()
        else:
            base_currency = match.group(3).upper()
            amount = match.group(4)

        conversion_result = converter.convert(amount, base_currency)
        await update.message.reply_text(conversion_result)
    else:
        await update.message.reply_text(languages[selected_language]['invalid_format'])
