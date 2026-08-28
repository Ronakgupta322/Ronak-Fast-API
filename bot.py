import os
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database


# ==============================
# CONFIG
# ==============================

API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

app = Client(
    "RonakKeyBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ==============================
# START
# ==============================

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"

    api_key, expiry_date, is_new = await database.get_or_create_key(user_id)

    now = datetime.now()

    days_left = max(0, (expiry_date - now).days)

    created_date = expiry_date - timedelta(days=30)

    created_str = created_date.strftime("%d %b %Y")
    expiry_str = expiry_date.strftime("%d %b %Y")

    # 30 Day Subscription Progress
    used_days = max(0, 30 - days_left)
    progress = min(10, max(0, int(used_days / 3)))

    progress_bar = "━" * progress + "●" + "━" * (9 - progress)


    # ==============================
    # PREMIUM UI
    # ==============================

    text = (
        "╭─────────────────────────╮\n"
        "│   ✦ 𝐑𝐎𝐍𝐀𝐊 𝐀𝐏𝐈 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 ✦   │\n"
        "╰─────────────────────────╯\n\n"

        f"👋 𝐖𝐞𝐥𝐜𝐨𝐦𝐞, {user_name}!\n"
        "🔐 Your API dashboard is ready.\n\n"

        "┌─「 🔑 𝐀𝐏𝐈 𝐊𝐄𝐘 」\n"
        "│\n"
        f"│  {api_key}\n"
        "│\n"
        "│  🟢 𝐒𝐭𝐚𝐭𝐮𝐬    : 𝐀𝐜𝐭𝐢𝐯𝐞\n"
        "│  ⚡ 𝐋𝐢𝐦𝐢𝐭     : 𝟑,𝟎𝟎𝟎 / 𝐝𝐚𝐲\n"
        "│\n"
        "└─────────────────────────\n\n"

        "┌─「 📊 𝐔𝐒𝐀𝐆𝐄 」\n"
        "│\n"
        "│  📡 Requests     │ 𝟎\n"
        "│  🎵 Audio        │ 𝟎\n"
        "│  🎬 Video        │ 𝟎\n"
        "│\n"
        "│  📈 Total        │ 𝟎\n"
        "│\n"
        "└─────────────────────────\n\n"

        "┌─「 💎 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍 」\n"
        "│\n"
        f"│  🗓 Created  : {created_str}\n"
        f"│  ⏳ Expires  : {expiry_str}\n"
        f"│  🔥 Remaining: {days_left} days\n"
        "│\n"
        f"│  {progress_bar}\n"
        "│\n"
        "└─────────────────────────\n\n"

        "⚡ 𝐅𝐚𝐬𝐭  •  𝐒𝐞𝐜𝐮𝐫𝐞  •  𝐑𝐞𝐥𝐢𝐚𝐛𝐥𝐞\n"
        "🔒 Keep your API key private."
    )


    # ==============================
    # BUTTONS
    # ==============================

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "♻️ 𝐑𝐄𝐍𝐄𝐖",
                callback_data="renew"
            ),
            InlineKeyboardButton(
                "🔑 𝐍𝐄𝐖 𝐊𝐄𝐘",
                callback_data="revoke"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 𝐃𝐎𝐂𝐒",
                url="https://t.me/MusicXUpdate"
            ),
            InlineKeyboardButton(
                "📢 𝐂𝐇𝐀𝐍𝐍𝐄𝐋",
                url="https://t.me/MusicXUpdate"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 𝐒𝐔𝐏𝐏𝐎𝐑𝐓",
                url="https://t.me/+SrpDLzodeAsyNGI8"
            )
        ]
    ])


    await message.reply_text(
        text,
        reply_markup=keyboard
    )


# ==============================
# CALLBACK
# ==============================

@app.on_callback_query()
async def callback_handler(client, query):

    if query.data == "renew":

        await query.answer(
            "♻️ Renewal system is currently under maintenance.",
            show_alert=True
        )

    elif query.data == "revoke":

        await query.answer(
            "🔑 New key generation is currently under maintenance.",
            show_alert=True
        )


# ==============================
# RUN
# ==============================

if name == "main":
    print("🚀 Ronak API Bot Started Successfully!")
    app.run()
