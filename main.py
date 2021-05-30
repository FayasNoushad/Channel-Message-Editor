import os
from pyrogram import Client, filters 

FayasNoushad = Client(
        "Channel Message Editor Bot",
        bot_token = os.environ["BOT_TOKEN"],
        api_id = int(os.environ["API_ID"]),
        api_hash = os.environ["API_HASH"]
)

@FayasNoushad.on_message(filters.private & filters.reply & (filters.media | filters.text))
async def post(bot, update): 
    if "-100" not in update.text:
        return
    try:
        await bot.copy_message(
            chat_id=update.text
            from_chat_id=update.reply_to_message.chat.id,
            message_id=update.reply_to_message.message_id,
            reply_markup=update.reply_to_message.reply_markup
        )
    except Exception:
        pass

FayasNoushad.run()
