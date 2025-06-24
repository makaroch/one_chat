
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.filters.chat_types import ChatTypesFilter
from src.filters.is_admin import IsAdmin
from src.states.admins import AdminAddNewContent
from src.settings import APP_SETTINGS

admin_private_router = Router()
admin_private_router.message.filter(ChatTypesFilter(["private"]), IsAdmin())


@admin_private_router.message(StateFilter(None), Command("load_new_free_content"))
async def new_pdf_file(message: Message, state: FSMContext):
    await message.answer("Отправьте новый файл, или введите 'Отмена'")
    await state.set_state(AdminAddNewContent.start)


@admin_private_router.message(AdminAddNewContent.start, F.document)
async def new_pdf_file(message: Message, state: FSMContext, bot: Bot):
    APP_SETTINGS.FILE_NAME = message.document.file_name
    path_save_file = f"src/data/{APP_SETTINGS.FILE_NAME}"
    await message.answer("Ожидайте...")

    await bot.download(
        file=message.document,
        destination=path_save_file
    )
    await state.clear()
    await message.answer("Записал новый файл")


@admin_private_router.message(AdminAddNewContent.start, F.text.lower() == "отмена")
async def new_xml_file(message: Message, state: FSMContext):
    await message.answer("Отменил ожидания нового файла")
    await state.clear()


@admin_private_router.message(AdminAddNewContent.start)
async def new_xml_file(message: Message, state: FSMContext):
    await message.answer("Ожидается новый документ. Попробуйте еще раз или введите 'Отмена'")
