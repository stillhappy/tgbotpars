from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON_RU['error'])