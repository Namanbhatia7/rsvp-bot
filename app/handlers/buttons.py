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
    choice = query.data

    state = redis_client.get(REDIS_KEY)
    if not state:
        await query.edit_message_text("No active poll.")
        return

    # Remove user from all categories first
    state['confirmed'] = [u for u in state['confirmed'] if u[0] != user_id]
    state['waitlist'] = [u for u in state['waitlist'] if u[0] != user_id]
    state['declined'] = [u for u in state['declined'] if u[0] != user_id]

    if choice == 'yes':
        if len(state['confirmed']) < state['limit']:
            state['confirmed'].append((user_id, name))
            await query.edit_message_text(f"You're confirmed, {name}! ✅")
        else:
            state['waitlist'].append((user_id, name))
            await query.edit_message_text(f"You're added to waitlist, {name}. ⏳")

    elif choice == 'no':
        state['declined'].append((user_id, name))
        await query.edit_message_text(f"You chose not to participate, {name}. ❌")

        # Promote from waitlist
        if len(state['confirmed']) < state['limit'] and state['waitlist']:
            promoted = state['waitlist'].pop(0)
            state['confirmed'].append(promoted)
            await context.bot.send_message(promoted[0], f"🎉 You're now confirmed for: {state['description']}")
    
    redis_client.set(REDIS_KEY, state)
