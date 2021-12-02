import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Channel Message Editor Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())

START_TEXT = """Hello {},
I am a channel message editor bot.

Made by @FayasNoushad"""
HELP_TEXT = """**More Help**

- I am a channel message editor bot.
- I can edit and post message of a channel.
- Use /post command with channel ID with reply a message for posting.
- Use /edit command with message link with reply a message for editing.

Made by @FayasNoushad"""
ABOUT_TEXT = """**About Me**

- **Bot :** `Channel Message Editor Bot`
- **Creator :** [Fayas](https://telegram.me/TheFayas)
- **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Channel-Message-Editor/tree/main)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Channel', url='https://telegram.me/FayasNoushad'),
            InlineKeyboardButton('Feedback', url='https://telegram.me/TheFayas')
        ],
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differnetly
    # (and we can only answer once),
    # so we don't always answer here.
    await update.answer("Processing")

    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if update.from_user.id not in AUTH_USERS:
        return
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.reply & filters.command(["post"]), group=1)
async def post(bot, update): 
    if ((update.text == "post") or (" " not in update.text)) or (update.from_user.id not in AUTH_USERS):
        return 
    if " " in update.text:
        chat_id = int(update.text.split()[1])
    try:
        user = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=update.from_user.id
        )
        if user.can_post_messages != True:
            await update.reply_text(
                text="You can't do that"
            )
            return
    except Exception:
        return
    try:
        post = await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=update.reply_to_message.chat.id,
            message_id=update.reply_to_message.message_id,
            reply_markup=update.reply_to_message.reply_markup
        )
        post_link = f"https://telegram.me/c/{post.chat.id}/{post.message_id}"
        await update.reply_text(
            text="Posted Successfully",
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton(text="Post", url=post_link)
                ]]
            )
        )
    except Exception as error:
        print(error)
        await update.reply_text(error)


@Bot.on_message(filters.private & filters.reply & filters.command(["edit"]), group=2)
async def edit(bot, update):
    if (update.text == "/edit") or (update.from_user.id not in AUTH_USERS):
        return
    if " " in update.text:
        command, link = update.text.split(" ", 1)
    else:
        return
    if "/" in link:
        ids = link.split("/")
        chat_id = -100 + int(ids[-2])
        message_id = int(ids[-1])
    else:
        return
    try:
        user = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=update.from_user.id
        )
        if user.can_be_edited != True:
            await update.reply_text(
                text="You can't do that, User needed can_be_edited permission."
            )
            return
    except Exception as error:
        print(error)
        await update.reply_text(error)
        return
    if update.reply_to_message.text:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=update.reply_to_message.text,
                reply_markup=update.reply_to_message.reply_markup,
                disable_web_page_preview=True
            )
        except Exception as error:
            await update.reply_text(error)
    else:
        await update.reply_text("I can edit text only")


Bot.run()
