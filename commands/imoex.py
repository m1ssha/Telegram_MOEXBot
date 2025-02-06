from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from API.moex import get_imoex
from functions.plot import plot_moex_index

PERIODS = {
    "3 дня": 3,
    "Неделя": 7,
    "2 недели": 14,
    "Месяц": 30,
    "Полгода": 182,
    "Год": 365,
    "2 года": 730,
    "5 лет": 1825,
    "10 лет": 3650
}

user_messages = {}


def register_imoex(dp: Dispatcher):
    @dp.message(Command("imoex"))
    async def imoex_handler(message: Message):
        args = message.text.split()
        
        if len(args) > 1:
            days = args[1]
            if days.isdigit():
                days = int(days)
                await process_imoex(message, days)
            else:
                await ask_period_imoex(message)
        else:
            await ask_period_imoex(message)

    @dp.callback_query(lambda c: c.data.startswith("imoex_period_"))
    async def handle_period_selection(callback: CallbackQuery):
        _, _, days = callback.data.split("_")  # Теперь правильно разбираем строку
        days = int(days)

        await callback.message.edit_text(f"⏳ Загружаю график IMOEX за {days} дней...")
        await process_imoex(callback.message, days)
        await callback.answer()


async def ask_period_imoex(message: Message):
    """Показывает кнопки с выбором периода для индекса IMOEX."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=period, callback_data=f"imoex_period_{days}")] for period, days in PERIODS.items()
        ]
    )

    await message.answer("📅 Выберите период для индекса MOEX:", reply_markup=keyboard)


async def process_imoex(message: Message, days: int):
    """Обрабатывает запрос на получение графика индекса IMOEX за выбранный период."""
    photo = plot_moex_index(days)

    if photo:
        caption = f"📊 График индекса MOEX (IMOEX) за последние {days} дней"
        await message.answer_photo(photo=photo, caption=caption, parse_mode="HTML")
    else:
        await message.answer("❌ Ошибка при получении данных", parse_mode="HTML")
