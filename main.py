import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler


from app.constants import CONFIRM_DESCRIPTION, CONFIRM_LIMIT
from app.handlers.commands import confirm_description, handle_limit, new_match, start_poll, status
from app.handlers.buttons import handle_button

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.bot.set_my_commands([
        ("newmatch", "Start a new match"),
        ("status", "Check current participants"),
    ])

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("startpoll", start_poll)],
        states={
            CONFIRM_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_description)
            ],
            CONFIRM_LIMIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_limit)
            ],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("newmatch", new_match))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot running...")
    app.run_polling()