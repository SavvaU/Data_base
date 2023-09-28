from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext
from filters.states import RegistrationCredit, GetSum, GeTern

router = Router()
db = create_db()


@router.message(Command(commands="credit"))
async def credit_1(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer("Напиши свой паспорт")
    await state.set_state(RegistrationCredit.passport_number)


@router.message(RegistrationCredit.passport_number)
async def credit_2(msg: Message, state=FSMContext):
    try:
        if not db.get_cust_by_passport(int(msg.text)):
            await msg.answer("Нeобходимо зарегистрироваться")
        else:
            await state.update_data(passport_number=msg.text)
            if db.chek_customer_abbility(int(msg.text)):
                await msg.answer("Введите желаемую сумму кредита:")
                await state.set_state(GetSum.credit_sum)
            else:
                await msg.answer("Перед выдaчей кредита необходимо погасить задолжности по платежам")
                await state.clear()
    except ValueError:
        await msg.answer("Пасспорт введен не корректно! \n Введите номер паспорта повторно!")
        await state.set_state(RegistrationCredit.passport_number)


@router.message(GetSum.credit_sum)
async def credit_3(msg: Message, state=FSMContext):
    try:
        if not db.is_enough_maney(int(msg.text)):
            await msg.answer("Слишком большая сумма!\n Введите повторно.")
            await state.set_state(GetSum.credit_sum)
        else:
            await state.update_data(credit_sum=msg.text)
            await msg.answer("Bвведите срок кредита")
            await state.set_state(GeTern.credit_tern)
    except ValueError:
        await msg.answer("Инвалидный ввод")
        await state.clear()

@router.message(GeTern.credit_tern)
async def credit_4(msg: Message, state=FSMContext):
    if int(msg.text) > 2:
        data = await state.get_data()
        try:
            db.add_credit(int(data["passport_number"]), int(data["credit_sum"]), int(msg.text))
            await msg.answer("Кредит успешно выдан")
            await state.clear()
        except ValueError:
            await msg.answer("Ошибка, попробуйте снова")
            await state.clear()
    else:
        await msg.answer("Недопустимый срок")
        await state.set_state(GeTern.credit_tern)