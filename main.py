import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from app.handlers.commands import new_match, status
from app.handlers.buttons import handle_button

# Logging
logging.basicConfig(level=logging.INFO)


# Main
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.bot.set_my_commands([
        ("newmatch", "Start a new match"),
        ("status", "Check current participants"),
    ])

    app.add_handler(CommandHandler("newmatch", new_match))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot running...")
    app.run_polling()