from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_credit
from aiogram.fsm.context import FSMContext
from filters.states import CreditList


router = Router()
db = create_db()


@router.message(Command(commands="credit_list"))
async def credit_list_1(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer("Введите номер пасспорта")
    await state.set_state(CreditList.passport_number)


@router.message(CreditList.passport_number)
async def credit_list_2(msg: Message, state=FSMContext):
    try:
        await msg.answer(format_list_credit(db.get_credit_list()))
        await state.clear()
    except ValueError:
        await msg.answer("Пасспорт введен некорректно")
        await state.set_state(CreditList.passport_number)
