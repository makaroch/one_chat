import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import ChatJoinRequest, Message, CallbackQuery

from src.database.dao import ClientDao, MessagesDao
from src.filters.chat_types import ChatTypesFilter
from src.keyboards.repl_keyboards import create_hist_btn
from src.settings import APP_SETTINGS

user_channel_router = Router()
user_channel_router.message.filter(ChatTypesFilter(["group", "supergroup"]))


@user_channel_router.message(Command("get_all_user_chats"))
async def command_start_handler(message: Message, bot: Bot) -> None:
    all_user = ClientDao.find_all()
    for user in all_user:
        if user.id == APP_SETTINGS.ROOT_USER_ID:
            continue
        text = f"Чат: {user.username} | {user.id} | {user.first_name} | {user.last_name}"
        await message.answer(
            text=text,
            reply_markup=create_hist_btn(user.id)
        )
        await asyncio.sleep(1)
    await message.answer(f"Это все диалоги")


@user_channel_router.callback_query(F.data.startswith("hist_"))
async def echo_handler(call: CallbackQuery) -> None:
    user_id = int(call.data.split("_")[1])
    messages = MessagesDao.get_history(from_user_id=user_id, to_user_id=APP_SETTINGS.ROOT_USER_ID)
    text = ""
    some_cash = {}
    for msg in messages:
        if msg.from_user not in some_cash:
            some_cash[msg.from_user] = ClientDao.find_one_or_none(id=msg.from_user).username
        if len(text + msg.message) < 3500:
            text += f"{msg.date_create} | {some_cash.get(msg.from_user, msg.from_user)}: {msg.message}\n\n"
        else:
            await call.message.answer(text)
            text = ""
    if text != "":
        await call.message.answer(text)
