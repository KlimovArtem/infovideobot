import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger("main")

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    logger.debug("Полученно сообщение от пользователя")
    username = message.from_user.first_name
    await message.answer(f"Привет {username}! Я ИнфоВидеоБот, спрашивай не стесняйся.")
