import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger("main")

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    logger.info("Полученно сообщение от пользователя")
    logger.debug("Полученна комманда /start")
    username = message.from_user.first_name
    await message.answer(f"Привет {username}! Я ИнфоВидеоБот, спрашивай не стесняйся.")
