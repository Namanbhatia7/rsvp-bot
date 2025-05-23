from telegram import Update
from telegram.ext import ContextTypes
from app.utils.storage import redis_client
from app.constants import REDIS_KEY, MAX_CONFIRMED

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_id = user.id
    name = user.full_name

    state = redis_client.get(REDIS_KEY) or {"confirmed": [], "waitlist": []}

    if query.data == 'join':
        if any(uid == user_id for uid, _ in state['confirmed'] + state['waitlist']):
            await query.edit_message_text("You've already responded.")
            return
        if len(state['confirmed']) < MAX_CONFIRMED:
            state['confirmed'].append((user_id, name))
            redis_client.set(REDIS_KEY, state)
            await query.edit_message_text(f"You're in, {name}! ✅")
        else:
            state['waitlist'].append((user_id, name))
            redis_client.set(REDIS_KEY, state)
            await query.edit_message_text(f"Added to waitlist, {name}. ⏳")

    elif query.data == 'drop':
        msg = ""
        if (user_id, name) in state['confirmed']:
            state['confirmed'].remove((user_id, name))
            msg = f"You've been removed, {name}. 👋"
            if state['waitlist']:
                promoted = state['waitlist'].pop(0)
                state['confirmed'].append(promoted)
                await context.bot.send_message(promoted[0], "🎉 You're now confirmed for the match!")
        elif (user_id, name) in state['waitlist']:
            state['waitlist'].remove((user_id, name))
            msg = f"Removed from waitlist, {name}."
        else:
            msg = "You weren't in the list."
        redis_client.set(REDIS_KEY, state)
        await query.edit_message_text(msg)
