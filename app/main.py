import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import load_settings
from app.handlers import router
from app.services.storage import init_db


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()
    init_db()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
