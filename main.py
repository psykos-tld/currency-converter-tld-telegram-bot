from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import start, base, lang, handle_callback
import os
from dotenv import load_dotenv

load_dotenv()

token_bot = os.getenv("TOKEN_BOT")

def main():
    app = ApplicationBuilder().token(token_bot).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, base))
    app.add_handler(CommandHandler('lang', lang))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()


if __name__ == '__main__':
    main()
