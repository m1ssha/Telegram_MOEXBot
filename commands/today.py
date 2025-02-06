from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_moex_stock_history
from functions.plot import plot_moex_history_today
from _tickers import POPULAR_TICKERS


def register_today(dp: Dispatcher):
    @dp.message(Command("today"))
    async def today_handler(message: Message):
        args = message.text.split()

        if len(args) > 1:
            ticker = args[1].upper()
            await process_today(message, ticker)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=ticker, callback_data=f"today_{ticker}")] for ticker in POPULAR_TICKERS
                ]
            )
            await message.answer("📊 Выберите акцию или введите её тикер:", reply_markup=keyboard)

    @dp.callback_query(lambda c: c.data.startswith("today_"))
    async def handle_today_selection(callback: CallbackQuery):
        ticker = callback.data.split("_")[1]
        await callback.message.edit_text(f"⏳ Загружаю график для {ticker}...")

        await process_today(callback.message, ticker)
        await callback.answer()

async def process_today(message: Message, ticker: str):
    """Обрабатывает тикер: строит график цены за сегодня."""
    photo = plot_moex_history_today(ticker)

    if photo:
        caption = f"📊 График цен акции <b>{ticker}</b> за сегодня"
        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
    else:
        await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
