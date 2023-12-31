from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_cust
from aiogram.fsm.context import FSMContext


router = Router()
db = create_db()


@router.message(Command(commands="cust_list"))
async def customer_1(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer(format_list_cust(db.get_customers_list()))