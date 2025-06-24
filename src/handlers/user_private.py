from aiogram import Router, Bot
from aiogram.types import Message

from src.filters.chat_types import ChatTypesFilter
from src.settings import APP_SETTINGS
from src.database.dao import ClientDao, MessagesDao

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(["private"]))


@user_private_router.message()
async def reply_message(message: Message, bot: Bot) -> None:
    user = ClientDao.find_one_or_none(id=message.chat.id)
    if user is None:
        ClientDao.create(
            id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            date_create=message.date,
        )

    if message.reply_to_message is not None and message.chat.id == APP_SETTINGS.ROOT_USER_ID:
        if message.text:
            MessagesDao.create(
                message=message.text,
                from_user=APP_SETTINGS.ROOT_USER_ID,
                to_user=message.reply_to_message.forward_from.id,
                date_create=message.date,
            )
        if message.photo and message.caption:
            await bot.send_photo(
                chat_id=message.reply_to_message.forward_from.id,
                photo=message.photo[-1].file_id,
                caption=message.caption
            )
        elif message.photo:
            await bot.send_photo(
                chat_id=message.reply_to_message.forward_from.id,
                photo=message.photo[-1].file_id
            )
        elif message.sticker:
            await bot.send_sticker(
                chat_id=message.reply_to_message.forward_from.id,
                sticker=message.sticker.file_id
            )
        elif message.video and message.caption is None:
            await bot.send_video(
                chat_id=message.reply_to_message.forward_from.id,
                video=message.video.file_id
            )
        elif message.document and message.caption is None:
            await bot.send_document(
                chat_id=message.reply_to_message.forward_from.id,
                document=message.document.file_id
            )
        elif message.document and message.caption:
            await bot.send_document(
                chat_id=message.reply_to_message.forward_from.id,
                document=message.document.file_id,
                caption=message.caption
            )
        elif message.audio:
            if message.caption:
                await bot.send_audio(
                    chat_id=message.reply_to_message.forward_from.id,
                    audio=message.audio.file_id,
                    caption=message.caption
                )
            else:
                await bot.send_audio(
                    chat_id=message.reply_to_message.forward_from.id,
                    audio=message.audio.file_id
                )
        elif message.voice:
            await bot.send_voice(
                chat_id=message.reply_to_message.forward_from.id,
                voice=message.voice.file_id
            )
        elif message.video_note:
            await bot.send_video_note(
                chat_id=message.reply_to_message.forward_from.id,
                video_note=message.video_note.file_id
            )
        elif message.animation:
            await bot.send_animation(
                chat_id=message.reply_to_message.forward_from.id,
                animation=message.animation.file_id
            )
        elif message.video and message.caption:
            await bot.send_video(
                chat_id=message.reply_to_message.forward_from.id,
                video=message.video.file_id,
                caption=message.caption
            )
        else:
            await bot.send_message(
                chat_id=message.reply_to_message.forward_from.id,
                text=message.text
            )

    if message.chat.id != APP_SETTINGS.ROOT_USER_ID:
        MessagesDao.create(
            message=message.text,
            to_user=APP_SETTINGS.ROOT_USER_ID,
            from_user=message.chat.id,
            date_create=message.date,
        )
        await message.forward(
            chat_id=APP_SETTINGS.ROOT_USER_ID
        )
