import json
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8999438350:AAFA3Jst28_aSR3nHQIWAsL-TIKy16BBIeM"

DATA_FILE = "players.json"

players = {}

def load_players():
    global players
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            players = json.load(f)
    else:
        players = {}

def save_players():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if user_id not in players:
        players[user_id] = {
            "name": user.first_name,
            "level": 1,
            "xp": 0,
            "coins": 100,
            "hp": 100,
        }
        save_players()

    await update.message.reply_text(
        f"🥷 Welcome {user.first_name}!\n\n"
        "🎮 Naruto RPG\n\n"
        "/profile - پروفایل\n"
        "/train - تمرین\n"
        "/mission - مأموریت\n"
        "/help - راهنما"
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if user_id not in players:
        await update.message.reply_text("اول /start را بزن.")
        return

    p = players[user_id]

    await update.message.reply_text(
        f"👤 {p['name']}\n\n"
        f"⭐ Level: {p['level']}\n"
        f"✨ XP: {p['xp']}\n"
        f"🪙 Coins: {p['coins']}\n"
        f"❤️ HP: {p['hp']}"
    )

async def train(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if user_id not in players:
        await update.message.reply_text("اول /start را بزن.")
        return

    p = players[user_id]
    p["xp"] += 20

    if p["xp"] >= p["level"] * 100:
        p["xp"] = 0
        p["level"] += 1
        p["coins"] += 50
        save_players()
        await update.message.reply_text(
            f"🎉 Level Up!\nاکنون Level {p['level']} هستی."
        )
    else:
        save_players()
        await update.message.reply_text("💪 تمرین انجام شد. +20 XP")

async def mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if user_id not in players:
        await update.message.reply_text("اول /start را بزن.")
        return

    p = players[user_id]
    p["coins"] += 30
    p["xp"] += 10

    save_players()

    await update.message.reply_text(
        "✅ مأموریت انجام شد!\n🪙 +30 Coins\n✨ +10 XP"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n/profile\n/train\n/mission"
    )

def main():
    load_players()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("train", train))
    app.add_handler(CommandHandler("mission", mission))
    app.add_handler(CommandHandler("help", help_command))

    print("Naruto RPG Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
