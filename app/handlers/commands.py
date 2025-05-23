from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.storage import redis_client
from constants import REDIS_KEY


async def new_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = {"confirmed": [], "waitlist": []}
    redis_client.set(REDIS_KEY, state)
    keyboard = [[
        InlineKeyboardButton("✅ I'm in!", callback_data='join'),
        InlineKeyboardButton("❌ Drop me", callback_data='drop')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏏 Who's in for today's cricket match?", reply_markup=reply_markup)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = redis_client.get(REDIS_KEY)
    if not state:
        await update.message.reply_text("No participants yet.")
        return
    msg = "\n".join([
        "✅ Confirmed:",
        *[f"{i+1}. {name}" for i, (_, name) in enumerate(state['confirmed'])],
        "",
        "⏳ Waitlist:",
        *[f"{i+1}. {name}" for i, (_, name) in enumerate(state['waitlist'])]
    ])
    await update.message.reply_text(msg or "No participants yet.")