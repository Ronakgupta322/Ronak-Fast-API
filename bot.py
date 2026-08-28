import os
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database

# आपकी डिटेल्स
API_ID = 36735558 
API_HASH = "fcd0e09634ee9e526a8da20e6d295cad"
BOT_TOKEN = "8965216924:AAFhHrLtihYIBjFVIBtjggkwnGmYuYeSLg0"

app = Client("RonakKeyBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- मेन्यू कीबोर्ड जेनरेटर ---
def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 View Your Key", callback_data="view_key")],
        [InlineKeyboardButton("📊 Usage", callback_data="view_key")], # Usage और View Key दोनों एक ही पेज दिखाएंगे
        [
            InlineKeyboardButton("📚 API Docs", callback_data="api_docs"),
            InlineKeyboardButton("💬 Support ↗", url="https://t.me/+SrpDLzodeAsyNGI8")
        ],
        [InlineKeyboardButton("📢 Channel ↗", url="https://t.me/MusicXUpdate")]
    ])

# --- /start कमांड (Main Menu) ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    # बैकग्राउंड में की (Key) बन जाएगी अगर नहीं है
    await database.get_or_create_key(user_id)
    
    text = f"👋 **Welcome {message.from_user.mention}!**\n\n**Main Menu**"
    await message.reply_text(text, reply_markup=get_main_menu_keyboard())

# --- बटन क्लिक हैंडलर (Navigation) ---
@app.on_callback_query()
async def on_callback(client, query):
    user_id = query.from_user.id
    data = query.data

    if data == "main_menu":
        text = f"👋 **Welcome {query.from_user.mention}!**\n\n**Main Menu**"
        await query.message.edit_text(text, reply_markup=get_main_menu_keyboard())

    elif data == "view_key":
        api_key, expiry_date, _ = await database.get_or_create_key(user_id)
        
        now = datetime.now()
        days_left = (expiry_date - now).days
        days_left = max(days_left, 0) # 0 से कम न हो
            
        expiry_str = expiry_date.strftime("%d %b %Y, %I:%M %p IST")
        created_date = expiry_date - timedelta(days=30)
        created_str = created_date.strftime("%d %b %Y, %I:%M %p IST")

        text = (
            "🔑 **Your API Key**\n\n"
            "**API Key:**\n"
            f"`{api_key}`\n"
            "**Status:** 🟢 Active\n"
            "**Daily Limit:** 3,000\n\n"
            "**Today's Usage:**\n"
            "📊 Requests: 0\n"
            "🎵 Audio: 0\n"
            "🎬 Video: 0\n\n"
            "**All-Time Usage:**\n"
            "📊 Total Requests: 0\n"
            "🎵 Total Audio: 0\n"
            "🎬 Total Video: 0\n\n"
            f"**Created:** {created_str}\n"
            f"**Expires:** {expiry_str}\n"
            f"**Days Left:** {days_left} days"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Renew", callback_data="action_renew")],
            [InlineKeyboardButton("🔄 Revoke & Get New Key", callback_data="action_revoke")],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
        ])
        await query.message.edit_text(text, reply_markup=keyboard)

    elif data == "api_docs":
        text = (
            "**API Documentation**\n\n"
            "**Base URL:** `https://web-production-94922.up.railway.app`\n"
            "**Primary API:** `https://web-production-94922.up.railway.app/download`\n\n"
            "**Endpoint:** `GET /download`\n"
            "**Params:** `url`, `type` (audio/video), `api_key`\n\n"
            "A ready-to-use Python client (Youtube.py) is available below, "
            "showing exactly how to call the API for audio and video downloads."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬇️ Download Youtube.py", callback_data="dl_file")],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
        ])
        await query.message.edit_text(text, reply_markup=keyboard)

    elif data in ["action_renew", "action_revoke"]:
        await query.answer("यह फीचर जल्द ही उपलब्ध होगा!", show_alert=True)
        
    elif data == "dl_file":
        await query.answer("अपनी Youtube.py फाइल को सीधे कॉपी करके अपने म्यूजिक बॉट में इस्तेमाल करें!", show_alert=True)

if __name__ == "__main__":
    print("Ronak API Bot with Main Menu UI Started!")
    app.run()
