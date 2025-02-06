from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_moex_lastprice
from functions.plot import plot_moex_history
from commands._tickers import POPULAR_TICKERS

PERIODS = {
    "3 дня": 3,
    "Неделя": 7,
    "2 недели": 14,
    "Месяц": 30,
    "Полгода": 182,
    "Год": 365,
    "2 года": 730,
    "5 лет": 1825
}

user_messages = {}


def register_get(dp: Dispatcher):
    @dp.message(Command("get"))
    async def getmoex_handler(message: Message):
        args = message.text.split()
        
        if len(args) > 1:
            ticker = args[1].upper()
            await ask_period(message, ticker, delete_message=False)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=ticker, callback_data=f"get_{ticker}")] for ticker in POPULAR_TICKERS
                ]
            )
            msg = await message.answer("📊 Выберите акцию или введите её тикер:", reply_markup=keyboard)

            user_messages[message.chat.id] = msg.message_id  

    @dp.callback_query(lambda c: c.data.startswith("get_"))
    async def handle_ticker_selection(callback: CallbackQuery):
        ticker = callback.data.split("_")[1]

        if callback.message.chat.id in user_messages:
            try:
                await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=user_messages[callback.message.chat.id])
                del user_messages[callback.message.chat.id]
            except Exception:
                pass

        await ask_period(callback.message, ticker)
        await callback.answer()

    @dp.callback_query(lambda c: c.data.startswith("period_"))
    async def handle_period_selection(callback: CallbackQuery):
        _, ticker, days = callback.data.split("_")
        days = int(days)

        await callback.message.edit_text(f"⏳ Загружаю график {ticker} за {days} дней...")
        await process_ticker(callback.message, ticker, days)
        await callback.answer()


async def ask_period(message: Message, ticker: str, delete_message=True):
    """Показывает кнопки с выбором периода."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=period, callback_data=f"period_{ticker}_{days}")] for period, days in PERIODS.items()
        ]
    )

    await message.answer(f"📅 Выберите период для {ticker}:", reply_markup=keyboard)


async def process_ticker(message: Message, ticker: str, days: int):
    """Обрабатывает тикер: отправляет график за выбранный период."""
    photo = plot_moex_history(ticker, days)

    if photo:
        caption = f"📊 График цен <b>{ticker}</b> за последние {days} дней"
        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
    else:
        await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
