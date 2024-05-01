import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream, AudioQuality, Update
from YukkiMusic.utils.thumbnails import gen_thumb


from .utils.active import _clear_
from .play import pytgcalls

welcome = 20
close = 30


@Client.on_message(filters.video_chat_started, group=welcome)
@Client.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    try:
        await _clear_(message.chat.id)
        await pytgcalls.leave_group_call(message.chat.id)
    except:
        pass


@pytgcalls.on_left()
@pytgcalls.on_closed_voice_chat()
@pytgcalls.on_kicked()
async def handler(_, update: Update):
    try:
        await _clear_(update.chat_id)
    except Exception as e:
        logging.exception(e)


@pytgcalls.on_stream_end()
async def on_stream_end(pytgcalls, update: Update):
    chat_id = update.chat_id
    i = await Client.get_me()
    get = clonedb.get(chat_id)
    if not get:
        try:
            await _clear_(chat_id)
            return await pytgcalls.leave_group_call(chat_id)
        except:
            return
    else:
        process = await Client.send_message(
            chat_id=chat_id,
            text="» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴛʀᴀᴄᴋ ғʀᴏᴍ ᴏ̨ᴜᴇᴜᴇ...",
        )
        title = get[0]["title"]
        duration = get[0]["duration"]
        file_path = get[0]["file_path"]
        videoid = get[0]["videoid"]
        req_by = get[0]["req"]
        user_id = get[0]["user_id"]
        get.pop(0)

        stream = MediaStream(file_path, audio_parameters=AudioQuality.HIGH)

        try:
            await pytgcalls.change_stream(
                chat_id,
                stream,
            )
        except:
            await _clear_(chat_id)
            return await pytgcalls.leave_group_call(chat_id)

        img = await gen_thumb(videoid)
        await process.delete()
        await app.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"**➻ sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n‣ **ᴛɪᴛʟᴇ :** [{title[:27]}](https://t.me/{i.username}?start=info_{videoid})\n‣ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n‣ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {req_by}",
        )