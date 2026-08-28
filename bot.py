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

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    
    # की (Key) और एक्सपायरी डेट प्राप्त करें
    api_key, expiry_date, is_new = await database.get_or_create_key(user_id)
    
    # दिन कैलकुलेट करें
    now = datetime.now()
    days_left = (expiry_date - now).days
    if days_left < 0:
        days_left = 0
        
    # डेट को फॉर्मेट करें (e.g., 28 Aug 2026, 05:45 PM IST)
    expiry_str = expiry_date.strftime("%d %b %Y, %I:%M %p IST")
    
    # Created date का अंदाज़ा (30 दिन पीछे)
    created_date = expiry_date - timedelta(days=30)
    created_str = created_date.strftime("%d %b %Y, %I:%M %p IST")

    # टेक्स्ट को बिल्कुल आपके स्क्रीनशॉट जैसा डिज़ाइन किया है
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
    
    # चैनल, सपोर्ट और अन्य बटन्स
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Renew", callback_data="renew"),
            InlineKeyboardButton("🔄 Revoke & Get New Key", callback_data="revoke")
        ],
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/MusicXUpdate"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+SrpDLzodeAsyNGI8")
        ]
    ])

    await message.reply_text(text, reply_markup=keyboard)

# डमी कॉलबैक हैंडलर ताकि बटन्स पर क्लिक करने से एरर न आये
@app.on_callback_query()
async def on_callback(client, query):
    if query.data in ["renew", "revoke"]:
        await query.answer("यह फीचर अभी मेंटेनेंस में है!", show_alert=True)

if __name__ == "__main__":
    print("Ronak API Bot is running with the new UI...")
    app.run()
