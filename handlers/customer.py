from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext
from filters.states import RegistrationCustomer

router = Router()
db = create_db()


@router.message(Command(commands="reg"))
async def customer_1(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer("Напиши свой паспорт")
    await state.set_state(RegistrationCustomer.passport_number)


@router.message(RegistrationCustomer.passport_number)
async def customer_2(msg: Message, state=FSMContext):
    try:
        if not db.get_cust_by_passport(int(msg.text)):
            db.add_customer(msg.from_user.first_name, int(msg.text))
            await msg.answer("Регистрация прошла успешно!")
            await state.clear()
        else:
            await msg.answer("Акаунт уже зарегистрирован!")
            await state.clear()
    except ValueError:
        await msg.answer("Номер пасспорта введен некорректно!")
        await state.set_state(RegistrationCustomer.passport_number)


