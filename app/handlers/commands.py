from tracemalloc import start
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.storage import redis_client
from app.constants import REDIS_KEY, CONFIRM_DESCRIPTION, CONFIRM_LIMIT

async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new match poll."""
    await update.message.reply_text("📋 Please provide the poll description:")
    return CONFIRM_DESCRIPTION

async def confirm_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm the poll description."""
    description = update.message.text
    context.user_data['description'] = description
    await update.message.reply_text(f"📝 Description set to: {description}\nPlease provide the participant limit:")
    return CONFIRM_LIMIT

async def handle_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        limit = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number.")
        return CONFIRM_LIMIT

    description = context.user_data['description']
    state = {
        "description": description,
        "limit": limit,
        "confirmed": [],
        "waitlist": [],
        "declined": []
    }
    redis_client.set(REDIS_KEY, state)

    keyboard = [[
        InlineKeyboardButton("✅ Yes", callback_data='yes'),
        InlineKeyboardButton("❌ No", callback_data='no')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"🗳️ {description}\n\nSelect your response:", reply_markup=reply_markup)
    return ConversationHandler.END


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
        await update.message.reply_text("No active poll.")
        return

    msg = [f"📋 *{state['description']}*\n"]
    msg.append("✅ *Confirmed:*" if state['confirmed'] else "✅ Confirmed: -")
    msg.extend([f"{i+1}. {name}" for i, (_, name) in enumerate(state['confirmed'])])
    msg.append("\n⏳ *Waitlist:*" if state['waitlist'] else "\n⏳ Waitlist: -")
    msg.extend([f"{i+1}. {name}" for i, (_, name) in enumerate(state['waitlist'])])
    msg.append("\n❌ *Declined:*" if state['declined'] else "\n❌ Declined: -")
    msg.extend([f"{i+1}. {name}" for i, (_, name) in enumerate(state['declined'])])

    await update.message.reply_text("\n".join(msg), parse_mode='Markdown')