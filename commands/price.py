from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_moex_lastprice
from commands._tickers import POPULAR_TICKERS

user_messages = {}


def register_price(dp: Dispatcher):
    @dp.message(Command("price"))
    async def get_price_handler(message: Message):
        args = message.text.split()

        if len(args) > 1:
            ticker = args[1].upper()
            await send_price(message, ticker)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=ticker, callback_data=f"price_{ticker}")] for ticker in POPULAR_TICKERS
                ]
            )
            msg = await message.answer("📊 Выберите акцию или введите её тикер:", reply_markup=keyboard)

            user_messages[message.chat.id] = msg.message_id  

    @dp.callback_query(lambda c: c.data.startswith("price_"))
    async def handle_ticker_selection(callback: CallbackQuery):
        ticker = callback.data.split("_")[1]

        if callback.message.chat.id in user_messages:
            try:
                await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=user_messages[callback.message.chat.id])
                del user_messages[callback.message.chat.id]
            except Exception:
                pass

        await send_price(callback.message, ticker)
        await callback.answer()


async def send_price(message: Message, ticker: str):
    """Получает и отправляет актуальную цену акции."""
    price = get_moex_lastprice(ticker)

    if price is None:
        await message.answer(f"❌ Не удалось получить цену для {ticker}. Проверьте тикер и попробуйте снова.")
    else:
        answer = f"💰 <b>{ticker}</b> актуальная цена: <b>{price} RUB</b>"
        await message.answer(answer, parse_mode="HTML")
