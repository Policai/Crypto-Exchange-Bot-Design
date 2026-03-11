import os
import httpx
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

router = Router()
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")


@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Добро пожаловать! Для работы отправьте номер телефона.", reply_markup=kb)


@router.message(F.contact)
async def save_contact(message: Message):
    payload = {
        "telegram_id": message.from_user.id,
        "username": message.from_user.username,
        "phone_number": message.contact.phone_number,
        "ip": "telegram",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{BACKEND_URL}/users/register", json=payload)

    webapp_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Открыть обменник", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
    )
    await message.answer("Профиль создан. Откройте WebApp для работы.", reply_markup=webapp_kb)
