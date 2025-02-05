from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from API.moex import get_moex_lastprice

def register_getmoex(dp):
    @dp.message(Command("getmoex"))
    async def getmoex_handler(message: Message):
        price = get_moex_lastprice("MOEX")
        answer = f"Hello! MOEX last price is {price} RUB"
        await message.answer(answer, parse_mode="HTML")