import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from ollama import chat
from ollama import ChatResponse


logger = logging.getLogger("main")

router = Router()

history = [
    {
        "role": "system",
        "content": "Ты умный помошник, поздаровайся."
    }
]

@router.message(Command("start"))
async def start(message: Message):
    logger.info("Полученно сообщение от пользователя")
    logger.debug("Полученна комманда /start")
    response: ChatResponse = chat(model='gemma3', messages=history)
    await message.answer(response['message']['content'])

@router.message()
async def any_message(message: Message):
    logger.info("Полученно сообщение от пользователя")
    logger.debug(f"Полученна сообщение {message.text}")
    history.append(dict(role="user", content=message.text))
    logger.info("Генерация ответа...")
    response: ChatResponse = chat(model='gemma3', messages=history)
    logger.debug(f"Ответ модели {response['message']['content']}")
    await message.answer(response['message']['content'])
