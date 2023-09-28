from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext


router = Router()
db = create_db()


@router.message(Command(commands="polis"))
async def polis(msg: Message, state=FSMContext):
    data = db.check_customers()
    if len(data) == 0:
        await msg.answer("Все кредиторы молодцы!")
    else:
        res_list = ""
        for cust in data:
            res_list += "Заемщик " + str(cust[1]) + " пасспорт " + str(cust[2]) + "\nЗадержал три и более платежа!" + "\n\n"
        await msg.answer(res_list )