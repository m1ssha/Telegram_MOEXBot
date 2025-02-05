from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from API.moex import get_moex_stock_history
from functions.plot import plot_moex_history, plot_moex_history_1d

def register_today(dp):
    @dp.message(Command("today"))
    async def today_handler(message: Message):
        ticker = "MOEX"
        photo = plot_moex_history_1d(ticker)

        if photo:
            caption = f"📊 График цен акции {ticker} за сегодня"
            await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
        else:
            await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
