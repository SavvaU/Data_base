from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_credit, format_list_payment
from aiogram.fsm.context import FSMContext
from filters.states import CreditC1, CreditC2


router = Router()
db = create_db()


@router.message(Command(commands="credit_check"))
async def credit_check_1(msg: Message, state=FSMContext):
    await state.clear()
    db.create_fee()
    await msg.answer("Напиши свой паспорт")
    await state.set_state(CreditC1.passport_number)

@router.message(CreditC1.passport_number)
async def credit_check_2(msg: Message, state=FSMContext):
    try:
        list_credits = db.get_credit_list_by_passport(int(msg.text))
        msg_list = format_list_credit(list_credits)
        await msg.answer("Список ваши кредитов\n" + msg_list + "\nВведите id интересующего кредита")
        await state.set_state(CreditC2.credit_id)
    except ValueError:
        await msg.answer("Пасспорт введен некорректно")
        await state.set_state(CreditC1.passport_number)


@router.message(CreditC2.credit_id)
async def credit_check_3(msg: Message, state=FSMContext):
    try:
        data = db.check_credit(int(msg.text))
        if len(data) > 0:
            pay_list = format_list_payment(data)
            await msg.answer("Кредит выплачен не полностью: оаталось " + str(len(data)) + " платежей\n" + pay_list)
            await state.clear()
        else:
            await msg.answer("Кредит полностью выплачен!\nБанк не имеет притензий к заёмщику!")
            await state.clear()
    except ValueError:
        await msg.answer("Данные некорректны!")
