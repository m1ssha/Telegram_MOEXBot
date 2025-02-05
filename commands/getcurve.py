from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from API.moex import get_moex_stock_history
from functions.plot import plot_moex_history

def register_getcurve(dp):
    @dp.message(Command("getcurve"))
    async def getcurve_handler(message: Message):
        ticker = "MOEX"
        days = 31
        photo = plot_moex_history(ticker, days=days)

        if photo:
            caption = f"📊 График цен акции {ticker} за последние {days} дней"
            await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
        else:
            await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
