import logging
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from Zaid import app, API_ID, API_HASH

user_sessions = {}
active_sessions = []

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["SessionDB"]
sessions_col = db["UserSessions"]

Button and message data
class Data:
    add_single_button = [InlineKeyboardButton("⛈️ ʜᴏsᴛ ᴏɴ ʏᴏᴜʀ ɪᴅ ⛈️", callback_data="add")]
    generate_single_button = [InlineKeyboardButton("⛈️ ʜᴏsᴛ ᴏɴ ʏᴏᴜʀ ɪᴅ ⛈️", callback_data="add")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")]
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("🕸️ sᴇssɪᴏɴ ʙᴏᴛ 🕸️", url="https://t.me/StringSesssionGeneratorRobot")],
        [
            InlineKeyboardButton("❔ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ", callback_data="help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ 🎶", callback_data="about")
        ],
        [
            InlineKeyboardButton("⚡ ᴜᴘᴅᴀᴛᴇ's ", url="https://t.me/Shivansh474"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ⛈️️", url="https://t.me/MASTIWITHFRIENDSXD")
        ],
        [InlineKeyboardButton("🌿 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🌿", url="https://t.me/SHIVANSHDEVS")],
    ]

    START = """
**┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞‌‌‌‌★
┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝛅ᴛʀᴀɴɢᴇʀ ꭙ 𝐔sᴇʛвσᴛ](https://t.me/StrangerUBbot)
┆● ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ ! 
└─────────────────────────•
❖ ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ɪᴅ-ᴜsᴇʀ-ʙᴏᴛ
❖ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ғᴏʀ ғᴜɴ. 
❖ ɪ ᴄᴀɴ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ 
•─────────────────────────•
❖ ʙʏ : [sᴛʀᴀɴɢᴇʀ ᴀssᴏᴄɪᴀᴛɪᴏɴ](https://t.me/StrangerAssociation) 🚩**
"""

    HELP = """
**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ** ⚡

/start - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
/help - ᴏᴘᴇɴ ʜᴇʟᴘ ᴍᴇɴᴜ
/about - ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴏᴡɴᴇʀ
/add - ᴀᴜᴛᴏ-ʜᴏsᴛ ᴛʜᴇ ʙᴏᴛ
/clone - ᴄʟᴏɴᴇ ᴠɪᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ
/remove - ʟᴏɢᴏᴜᴛ ғʀᴏᴍ ʙᴏᴛ
"""

    ABOUT = """
**ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ** 🌙

ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴛᴏ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ ᴡɪᴛʜ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴɪᴍᴀᴛɪᴏɴ.

sᴜᴘᴘᴏʀᴛᴇᴅ: ʀᴇᴘʟʏ-ʀᴀɪᴅ, ɪᴅ-ᴄʟᴏɴᴇ, ʀᴀɪᴅ, sᴘᴀᴍ, ᴜsᴇʀ-ᴛᴀɢɢᴇʀ ʟᴏᴠᴇ-ʀᴀɪᴅ(sʜᴀʀʏɪ) ᴀɴᴅ ᴀʟsᴏ.

◌ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ](https://www.python.org)

◌ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [sʜɪᴠᴀɴsʜ-xᴅ](https://t.me/SHIVANSH474)

◌ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [sʜɪᴠᴀɴsʜ](https://t.me/SHIVANSHDEVS)
"""

# /start command
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    reply_markup = InlineKeyboardMarkup(Data.buttons)
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=reply_markup
    )

# /help command
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text(
        Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# /about command
@app.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    await message.reply_text(
        Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# Callback query handler
@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "home":
        await query.message.edit_media(
            media=InputMediaPhoto(ALIVE_PIC, caption=Data.START),
            reply_markup=InlineKeyboardMarkup(Data.buttons)
        )
    elif data == "help":
        await query.message.edit_text(
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    elif data == "about":
        await query.message.edit_text(
            Data.ABOUT,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )

async def restart_all_sessions():
    logging.info("ʀᴇsᴛᴀʀᴛɪɴɢ ᴀʟʟ ᴜsᴇʀ's ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴs...")
    sessions = sessions_col.find()
    for session in sessions:
        try:
            uid = session["user_id"]
            string = session["session"]
            client = Client(
                name=f"AutoClone_{uid}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules")
            )
            await client.start()
            active_sessions.append(client)
            logging.info(f"sᴛᴀʀᴛᴇᴅ sᴇssɪᴏɴ ғᴏʀ ᴜsᴇʀ {uid}")
        except Exception as e:
            logging.error(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴛᴀʀᴛ sᴇssɪᴏɴ ғᴏʀ ᴜsᴇʀ {uid}: {e}")

@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    reply_markup = InlineKeyboardMarkup(Data.buttons)
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=reply_markup)

@app.on_message(filters.command("clone"))
async def clone(bot: app, msg: Message):
    chat = msg.chat
    text = await msg.reply("❍ FIRST GEN SESSION \n\n𔓕 /clone session\n\nOR - USE  \n\n𔓕 /add (ғᴏʀ ᴀᴜᴛᴏ-ʜᴏsᴛ)")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
        
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="Zaid/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"❖ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ʀᴇᴀᴅʏ ᴛᴏ ғɪɢʜᴛ\n\n❍ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ\n\n❖ {user.first_name}")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\n ᴘʀᴇss /start ᴛᴏ sᴛᴀʀᴛ ᴀɢᴀɪɴ.")

@app.on_message(filters.command("add"))
async def add_session(_, msg: Message):
    await msg.reply("📲 ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (e.g., +918200000009):")
    user_sessions[msg.from_user.id] = {"step": "awaiting_phone"}

@app.on_message(filters.command("remove"))
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})
    if not session_data:
        return await msg.reply("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴ ғᴏᴜɴᴅ.")

    try:
        for client in active_sessions:
            if client.name == f"AutoClone_{uid}":
                await client.stop()
                active_sessions.remove(client)
                break
        sessions_col.delete_one({"_id": uid})
        await msg.reply("✅ ʏᴏᴜʀ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
    except Exception as e:
        await msg.reply(f"⚠️ ᴇʀʀᴏʀ ᴛᴏ ʀᴇᴍᴏᴠɪɴɢ sᴇssɪᴏɴ:\n`{e}`")

@app.on_message()
async def session_handler(_, msg: Message):
    uid = msg.from_user.id
    session = user_sessions.get(uid)
    if not session:
        return

    step = session.get("step")
    if step == "awaiting_phone":
        phone = msg.text.strip()
        client = Client(name=f"gen_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})
        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sᴇɴᴛ! ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ: `1 2 3 4 5` ( sᴘᴀᴄᴇ ʙʏ sᴘᴀᴄᴇ )")
        except Exception as e:
            await msg.reply(f"❌ ᴏᴛᴘ ᴡᴀs ᴡʀᴏɴɢ ᴏʀ ᴇxᴘɪʀᴇᴅ :\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        otp = msg.text.strip()
        client = session["client"]
        try:
            await client.sign_in(phone_number=session["phone"], phone_code_hash=session["phone_code_hash"], phone_code=otp)
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            return await msg.reply("🔐 sᴇɴᴅ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ.")
        except Exception as e:
            await msg.reply(f"❌ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ ᴡʀᴏɴɢ ғᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ:\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return
        await finalize_login(client, msg, uid)

    elif step == "awaiting_2fa":
        password = msg.text.strip()
        client = session["client"]
        try:
            await client.check_password(password)
            await finalize_login(client, msg, uid)
        except Exception as e:
            await msg.reply(f"❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ:\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

async def finalize_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()

        sessions_col.update_one(
            {"_id": uid},
            {"$set": {
                "session": string,
                "name": user.first_name,
                "user_id": user.id,
                "username": user.username
            }},
            upsert=True
        )

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        active_sessions.append(hosted)

        await msg.reply(f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n\n🔐 sᴇssɪᴏɴ sᴛʀɪɴɢ:\n\n`{string}`\n\nᴀᴜᴛᴏ-ʜᴏsᴛ ɴᴏᴡ..\n\n|| 🔪ᴛᴏ ʙᴏᴛ ғʀᴏᴍ ʏᴏᴜʀ ɪᴅ sᴇɴᴅ ᴛʜɪs ᴄᴍᴅ  /remove .... ||")
    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ \nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)