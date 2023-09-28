from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_credit
from aiogram.fsm.context import FSMContext
from filters.states import Pay1, Pay2, Pay3

router = Router()
db = create_db()


@router.message(Command(commands="pay"))
async def pay_1(msg: Message, state=FSMContext):
    await state.clear()
    db.create_fee()
    await msg.answer("Напиши свой паспорт")
    await state.set_state(Pay1.passport_number)

@router.message(Pay1.passport_number)
async def pay_2(msg: Message, state=FSMContext):
    try:
        list_credits = db.get_credit_list_by_passport(int(msg.text))
        msg_list = format_list_credit(list_credits)
        await msg.answer("Список ваши кредитов\n" + msg_list + "\nВведите id интересующего кредита")
        await state.set_state(Pay2.credit_id)
    except ValueError:
        await msg.answer("Пасспорт введен некорректно")
        await state.set_state(Pay1.passport_number)

@router.message(Pay2.credit_id)
async def pay_3(msg: Message, state=FSMContext):
    try:
        data = db.get_payments_list_by_id_pay(int(msg.text))
        if len(data) == 0:
            await msg.answer("Кредит уже погашен")
            return
        await msg.answer("Сумма платежа: " + str(data[0][1]) + "\nв том числе пени: " + str(data[0][2]) + "\nВнести плтаеж?")
        await state.update_data(pay_id=data[0][0])
        await state.set_state(Pay3.yes_no)
    except ValueError:
        await msg.answer("Некорректый id!")


@router.message(Pay3.yes_no)
async def pay_4(msg: Message, state=FSMContext):
    if msg.text.lower() == "да":
        data = await state.get_data()
        db.close_pay(data["pay_id"])
        await msg.answer("Платеж внесен успешно")
        await state.clear()
    else:
        await msg.answer("Хорошо, досвидания!")
        await state.clear()