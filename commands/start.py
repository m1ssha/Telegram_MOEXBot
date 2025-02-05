import logging
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

def register_start(dp):
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        answer = f"Выберите команду из предложенных вариантов"
        await message.answer(answer, parse_mode="HTML")
