import asyncio
import logging
import logging.config as logging_config
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session import aiohttp
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import yaml

import routers


load_dotenv()

try:
    with open('../.log-config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        logging_config.dictConfig(config)
except yaml.YAMLError as e:
    logging.exception(
        f"Ошибка в файле .log-config.yaml.\n{e}")
except FileNotFoundError as e:
    logging.exception(
        f"Файл .log-config.yaml не найден проверь путь к файлу.\n {e}"
    )
except Exception as e:
    logging.exception(e)

logger = logging.getLogger("main")

async def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Переменная BOT_TOKEN не определена.")
        logger.error("Переменная BOT_TOKEN не определена.")

    session = aiohttp.AiohttpSession(proxy="http://proxy.server:3128")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session
    )

    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(routers.router)
    logger.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

