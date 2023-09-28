from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext


router = Router()
db = create_db()


@router.message(Command(commands="fin"))
async def fin(msg: Message, state=FSMContext):
    await msg.answer(db.fin_upd())