import os
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.helper.basic import edit_or_reply, get_text, get_user
from Zaid.modules.help import add_command_help
from Zaid.helper.functions import user_only, user_errors, delete_reply  

FName = ""
LName = ""
Bio = ""

@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone_user(client: Client, message: Message):
    global FName, LName, Bio

    try:
        user = await user_only(client, message, Owner, Sudos)
        if not user:
            return
    except Exception as er:
        await message.reply(user_errors(er))
        return

    me = await client.get_me()
    FName = me.first_name
    LName = me.last_name if me.last_name else ""
    me_chat = await client.get_chat("me")
    Bio = me_chat.bio if me_chat.bio else ""

    reply_msg = await message.reply("Cloning...")

    user_chat = await client.get_chat(user.id)
    user_bio = user_chat.bio if user_chat.bio else None

    pic = None
    if user.photo:
        try:
            pic = await client.download_media(user.photo.big_file_id)
        except Exception as e:
            await reply_msg.edit(f"Failed to download photo: {e}")

    try:
        if pic:
            await client.set_profile_photo(photo=pic)
        if user.last_name:
            await client.update_profile(first_name=user.first_name, last_name=user.last_name, bio=user_bio)
        else:
            await client.update_profile(first_name=user.first_name, bio=user_bio)

        await delete_reply(message, reply_msg, f"Now I'm {user.first_name}!\n\nNote: Don't restart until you revert me!")
    except Exception as error:
        await delete_reply(message, reply_msg, str(error))

@Client.on_message(filters.command("revert", ".") & filters.me)
async def _revert(client: Client, message: Message):
    global FName, LName, Bio

    if not FName:
        await message.reply("Error: You haven't cloned anyone!")
        return

    reply_msg = await message.reply("Reverting...")
    user_bio = Bio or "💕ɪ ᴀᴍ ᴘᴀʀᴛ ᴏғ sᴛʀᴀɴɢᴇʀ💕"

    try:
        if LName:
            await client.update_profile(first_name=FName, last_name=LName, bio=user_bio)
        else:
            await client.update_profile(first_name=FName, bio=user_bio)

        photos = [x async for x in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos(photos[0].file_id)

        await delete_reply(message, reply_msg, "I'm back!")

        FName = ""
        LName = ""
        Bio = ""

    except Exception as error:
        await delete_reply(message, reply_msg, str(error))

add_command_help(
    "clone",
    [
        ["clone", "Clone someone’s profile (name, bio, photo). Reply to a user or use `.clone <username>`."],
        ["revert", "Restore your original profile (name, bio, photo)."],
    ],
)