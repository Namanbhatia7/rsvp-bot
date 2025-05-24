# 🏏 Telegram RSVP Bot

A simple Telegram bot to manage RSVPs for group activities like cricket matches.  
Only a limited number of participants can confirm, others go to a waitlist.

---

## ✨ Features

- `/newmatch` — Start a new RSVP session
- `/status` — View current list of confirmed and waitlisted users
- ✅ Button — Join the match (if full, added to waitlist)
- ❌ Button — Drop out (waitlist users are promoted)

---

## 🚀 Live Deployment

- **Bot Hosting**: [Render.com](https://render.com/)
- **Redis**: [Upstash](https://upstash.com/)

---

## 🛠️ Setup Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-rsvp-bot.git
cd telegram-rsvp-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_SSL=
```

### 4. Run the bot

```bash
python -m telegram_rsvp_bot
```
