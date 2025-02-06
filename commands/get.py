from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_moex_lastprice
from functions.plot import plot_moex_history_today
from _tickers import POPULAR_TICKERS


def register_get(dp: Dispatcher):
    @dp.message(Command("get"))
    async def getmoex_handler(message: Message):
        args = message.text.split()
        
        if len(args) > 1:
            ticker = args[1].upper()
            await process_ticker(message, ticker)
            return
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=ticker, callback_data=f"get_{ticker}")] for ticker in POPULAR_TICKERS
                ]
            )
            await message.answer("📊 Выберите акцию или введите её тикер:", reply_markup=keyboard)

    @dp.callback_query(lambda c: c.data.startswith("get_"))
    async def handle_ticker_selection(callback: CallbackQuery):
        ticker = callback.data.split("_")[1]
        await callback.message.edit_text(f"⏳ Загружаю данные для {ticker}...")

        await process_ticker(callback.message, ticker)
        await callback.answer()

async def process_ticker(message: Message, ticker: str):
    """Обрабатывает тикер: отправляет цену и график."""
    price = get_moex_lastprice(ticker)
    photo = plot_moex_history_today(ticker)

    if price is None:
        await message.answer("❌ Не удалось получить данные. Проверьте тикер.")
    else:
        answer = f"📈 <b>{ticker}</b> последняя цена: <b>{price} RUB</b>"
        await message.answer_photo(photo=photo, caption=answer, parse_mode="HTML")
