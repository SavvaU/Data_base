from aiogram import Router, Bot, F
from aiogram.types import Message

router = Router()

@router.message()
async def echo(msg:Message):
    await msg.answer("Ильсаф ЛОх")