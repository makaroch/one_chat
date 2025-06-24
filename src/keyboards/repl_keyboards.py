from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder



def create_hist_btn(user_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=f"Посмотреть историю сообщений",
            callback_data=f"hist_{user_id}",
        )
    )

    return keyboard.as_markup()
