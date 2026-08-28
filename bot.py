import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database

# अपनी डिटेल्स यहाँ डालें
API_ID = 1234567 
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

app = Client("RonakKeyBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    
    # यह फंक्शन आटोमेटिक चेक करेगा कि 30 दिन हुए या नहीं
    api_key, expiry_date, is_new = await database.get_or_create_key(user_id)
    
    expiry_str = expiry_date.strftime("%d %b %Y, %I:%M %p")
    
    text = f"👋 **Welcome {message.from_user.mention}!**\n\n"
    if is_new:
        text += "✅ **आपकी नई API Key जनरेट कर दी गई है!**\n\n"
    else:
        text += "✅ **आपकी API Key पहले से एक्टिव है:**\n\n"
        
    text += f"🔑 **Key:** `{api_key}`\n"
    text += f"⏳ **Expires On:** `{expiry_str}` (30 Days)\n\n"
    text += "⚠️ *अगर 30 दिन पूरे हो गए, तो /start दबाने पर आपको आटोमेटिक नई Key मिल जाएगी।*"

    await message.reply_text(text)

if __name__ == "__main__":
    app.run()
