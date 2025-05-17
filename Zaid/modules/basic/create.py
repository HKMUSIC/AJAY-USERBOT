from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.modules.help import add_command_help


@Client.on_message(filters.command("create", ".") & filters.me)
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("**Usage:** `.create [gc/ch] [name]`\nExample: `.create gc My Group`")

    group_type = message.command[1].lower()
    group_name = " ".join(message.command[2:])
    xd = await message.edit_text("`Processing...`")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")

    if group_type == "gc":  # for supergroup
        chat = await client.create_supergroup(group_name, desc)
    elif group_type == "ch":  # for channel
        chat = await client.create_channel(group_name, desc)
    else:
        return await xd.edit("**Invalid type!** Use `gc` for group or `ch` for channel.")

    await xd.edit(
        f"**Successfully Created Telegram {'Group' if group_type == 'gc' else 'Channel'}:** "
        f"[{group_name}]({chat.invite_link})",
        disable_web_page_preview=True,
    )


add_command_help(
    "create",
    [
        ["create ch <name>", "Create a channel with the given name."],
        ["create gc <name>", "Create a group with the given name."],
    ],
)
