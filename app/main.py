import asyncio
import logging

from aiogram import F
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from pathlib import Path

from app.config import load_settings
from pathlib import Path
DATA_DIR = Path("data")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Salom! Bot ishga tushdi.")

@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "/start - Botni ishga tushurish\n"
        "/help - Yordam olish"
    )

@router.message(F.document)
async def file_handler(message: Message) -> None:
    doc = message.document
    # TODO: file_name None bo‘lsa fallback nom beramiz
    file_name = doc.file_name or f"file_{doc.file_id}"
    file_path = DATA_DIR / file_name

    file = await message.bot.get_file(doc.file_id)
    await message.bot.download_file(file.file_path, destination=file_path)

    # TODO: keyin format tanlash (inline buttons)
    await message.answer(f"Qabul qilindi: {file_name}")

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()
    
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
