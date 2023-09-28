from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_credit, format_list_payment
from aiogram.fsm.context import FSMContext
from filters.states import PaymentsList, PaymentsListId

router = Router()
db = create_db()


@router.message(Command(commands="payments_list"))
async def payments_list_1(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer("Введите номер пасспорта")
    await state.set_state(PaymentsList.passport_number)


@router.message(PaymentsList.passport_number)
async def payments_list_2(msg: Message, state=FSMContext):
    try:
        list_credits = db.get_credit_list_by_passport(int(msg.text))
        msg_list = format_list_credit(list_credits)
        await msg.answer("Список ваши кредитов\n" + msg_list + "\nВведите id интересующего кредита")
        await state.set_state(PaymentsListId.credit_id)
    except ValueError:
        await msg.answer("Пасспорт введен некорректно")
        await state.set_state(PaymentsList.passport_number)

@router.message(PaymentsListId.credit_id)
async def payments_list_3(msg: Message, state=FSMContext):
    try:
        data = db.get_payments_list_by_id(int(msg.text))
        if not data:
            await msg.answer("id введен некорректно!")
        else:
            msg_list = format_list_payment(data)
            await msg.answer(msg_list)
            await state.clear()
    except ValueError:
        await msg.answer("некорректный ввод!")


# @router.message(PaymentsListId.credit_id)
# async def payments_list_3
