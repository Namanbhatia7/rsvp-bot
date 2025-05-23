import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from handlers.commands import new_match, status
from handlers.buttons import handle_button

# Logging
logging.basicConfig(level=logging.INFO)