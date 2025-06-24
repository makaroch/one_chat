from aiogram import Router

from src.handlers.user_group import user_channel_router
from src.handlers.user_private import user_private_router

handlers_router = Router()

handlers_router.include_routers(
    user_private_router,
    user_channel_router,
)
