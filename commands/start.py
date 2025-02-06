import logging
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from messages import messages

def register_start(dp):
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        answer = messages.welcome_message
        await message.answer(answer, parse_mode="HTML", disable_web_page_preview=True)