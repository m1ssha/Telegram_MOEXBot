import logging
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

def register_start(dp):
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        answer = f"use /help to get help"
        await message.answer(answer, parse_mode="HTML")