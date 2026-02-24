import os
import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types.input_file import FSInputFile

from app.services.conversion import pdf_to_png_zip, png_to_pdf
from app.services.storage import get_last_upload, save_upload
from app.utils.files import DATA_DIR, safe_rmdir, safe_unlink

router = Router()
POPPLER_PATH = os.getenv("POPPLER_PATH")
logger = logging.getLogger(__name__)

MAX_MB = 10
ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg"}


def is_allowed(filename: str, size: int) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXT and size <= MAX_MB * 1024 * 1024


def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="PDF -> PNG", callback_data="convert:pdf2png")],
        [InlineKeyboardButton(text="PNG -> PDF", callback_data="convert:png2pdf")],
    ])


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
    file_name = doc.file_name or f"file_{doc.file_id}"
    if not is_allowed(file_name, doc.file_size or 0):
        await message.answer("Fayl turi yoki hajmi ruxsat etilmagan.")
        return
    file_path = DATA_DIR / file_name

    file = await message.bot.get_file(doc.file_id)
    await message.bot.download_file(file.file_path, destination=file_path)

    save_upload(message.from_user.id, str(file_path))
    await message.answer(f"Qabul qilindi: {file_name}")
    await message.answer("Format tanlang:", reply_markup=build_keyboard())


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    photo = message.photo[-1]
    file_name = f"photo_{photo.file_id}.png"
    if not is_allowed(file_name, photo.file_size or 0):
        await message.answer("Rasm hajmi ruxsat etilmagan.")
        return
    file_path = DATA_DIR / file_name

    file = await message.bot.get_file(photo.file_id)
    await message.bot.download_file(file.file_path, destination=file_path)

    save_upload(message.from_user.id, str(file_path))
    await message.answer("Format tanlang:", reply_markup=build_keyboard())


@router.callback_query(F.data.startswith("convert:"))
async def convert_choice(callback: CallbackQuery) -> None:
    try:
        user_id = callback.from_user.id
        src_path = get_last_upload(user_id)

        if not src_path:
            await callback.message.answer("Oldin fayl yuboring.")
            await callback.answer()
            return

        if callback.data == "convert:png2pdf":
            pdf_path = png_to_pdf(src_path)
            await callback.message.answer_document(document=FSInputFile(pdf_path))
            safe_unlink(Path(src_path))
            safe_unlink(Path(pdf_path))
            await callback.answer()
            return

        if callback.data == "convert:pdf2png":
            if not src_path.lower().endswith(".pdf"):
                await callback.message.answer("Bu fayl PDF emas.")
                await callback.answer()
                return

            base_name = Path(src_path).stem
            out_dir = DATA_DIR / f"{base_name}_pages"
            zip_path, png_paths = pdf_to_png_zip(src_path, out_dir, POPPLER_PATH)
            await callback.message.answer_document(document=FSInputFile(str(zip_path)))
            for p in png_paths:
                safe_unlink(p)
            safe_unlink(zip_path)
            safe_rmdir(out_dir)
            await callback.answer()
            return

        await callback.message.answer("Bu format hozircha yo‘q.")
        await callback.answer()
    except Exception as e:
        logger.exception("convert error: %s", e)
        await callback.message.answer("Xatolik bo‘ldi. Keyinroq urinib ko‘ring.")
        await callback.answer()
