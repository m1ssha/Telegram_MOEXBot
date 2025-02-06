from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_moex_stock_history
from functions.plot import plot_moex_history
from _tickers import POPULAR_TICKERS

def register_getcurve(dp: Dispatcher):
    @dp.message(Command("getcurve"))
    async def getcurve_handler(message: Message):
        args = message.text.split()
        
        if len(args) > 1:
            ticker = args[1].upper()
            await process_curve(message, ticker)
            return
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=ticker, callback_data=f"curve_{ticker}")] for ticker in POPULAR_TICKERS
                ]
            )
            await message.answer("📊 Выберите акцию или введите её тикер:", reply_markup=keyboard)

    @dp.callback_query(lambda c: c.data.startswith("curve_"))
    async def handle_curve_selection(callback: CallbackQuery):
        ticker = callback.data.split("_")[1]
        await callback.message.edit_text(f"⏳ Загружаю график для {ticker}...")

        await process_curve(callback.message, ticker)
        await callback.answer()

async def process_curve(message: Message, ticker: str, days: int = 31):
    """Обрабатывает тикер: строит график цены за 31 день."""
    photo = plot_moex_history(ticker, days=days)

    if photo:
        caption = f"📊 График цен акции <b>{ticker}</b> за последние {days} дней"
        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
    else:
        await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
