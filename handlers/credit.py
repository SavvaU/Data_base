from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext
from filters.states import RegistrationCredit, GetSum

router = Router()
db = create_db()


@router.message(Command(commands="credit"))
async def credit_1(msg: Message, state=FSMContext):
    await msg.answer("Напиши свой паспорт")
    await state.set_state(RegistrationCredit.passport_number)


@router.message(RegistrationCredit.passport_number)
async def credit_2(msg: Message, state=FSMContext):
    try:
        if db.is_this_customer_in_db(passport=int(msg.text)):
            await msg.answer("НЕобходимо зарегистрироваться")
        flag = db.chek_customer_abbility(int(msg.text))
        if not flag:
            await msg.answer("Перед выдочей кредита необходимо погасить задолжности по платежам")
        else:
            await msg.answer("Введите желаемую сумму кредита:")
            await state.set_state(GetSum.credit_sum)
    except ValueError:
        await msg.answer("Пасспорт введен не корректно!")


@router.message(GetSum.credit_sum)
async def credit_3(msg: Message, state=FSMContext):
    if int(msg.text) > 1000000:
        await msg.answer("Много хочешь!")



