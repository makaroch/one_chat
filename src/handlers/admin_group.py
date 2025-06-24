from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from src.filters.chat_types import ChatTypesFilter
from src.settings import APP_SETTINGS

admin_group_router = Router()
admin_group_router.message.filter(ChatTypesFilter(["group", "supergroup"]))


@admin_group_router.message(Command('admin'))
async def command_start_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    if str(chat_id) != str(APP_SETTINGS.ADMIN_GROUP_ID):
        return

    admin_lst = await bot.get_chat_administrators(chat_id)
    admin_lst = [
        item.user.id
        for item in admin_lst
        if item.status == "creator" or item.status == "administrator"
    ]
    if message.from_user.id not in admin_lst:
        await message.answer("Вы не администратор и не можете использовать эту команду")
        return
    bot.my_admins_lst = admin_lst
    await message.answer("Админы обновлены")
