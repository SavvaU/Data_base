from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db, format_list_credit
from aiogram.fsm.context import FSMContext
from filters.states import FPay1, FPay2, FPay4

router = Router()
db = create_db()


@router.message(Command(commands="fpay"))
async def f_pay_1(msg: Message, state=FSMContext):
    await state.clear()
    db.create_fee()
    await msg.answer("Напиши свой паспорт")
    await state.set_state(FPay1.passport_number)

@router.message(FPay1.passport_number)
async def f_pay_2(msg: Message, state=FSMContext):
    try:
        if not db.chek_customer_abbility(int(msg.text)):
            await msg.answer("Есть непогашенные платежи")
            await state.clear()
        else:
            list_credits = db.get_credit_list_by_passport(int(msg.text))
            msg_list = format_list_credit(list_credits)
            await msg.answer("Список ваши кредитов\n" + msg_list + "\nВведите id интересующего кредита")
            await state.set_state(FPay2.credit_id)
    except ValueError:
        await msg.answer("Пасспорт введен некорректно")
        await state.set_state(FPay1.passport_number)

@router.message(FPay2.credit_id)
async def f_pay_3(msg: Message, state=FSMContext):
    try:
        sum = db.check_credit_fp(int(msg.text))
        await state.update_data(sum=sum)
        await state.update_data(id=int(msg.text))
        if sum == 0:
            await msg.answer("Кредит уже погашен")
        else:
            await msg.answer("Остаток по кредиту " + str(sum) + "\nВведите сумму для погашения")
            await state.set_state(FPay4.fp_sum)
    except ValueError:
        await msg.answer("Айди кредита введен некорректно")

@router.message(FPay4.fp_sum)
async def f_pay_4(msg: Message, state=FSMContext):
    try:
        data = await state.get_data()
        sum = data["sum"]
        if int(msg.text) > sum:
            await msg.answer("Слишком большая сумма погашения, кредит будет погашен полностью")
            db.close_credit(sum, data["id"])
            await msg.answer("Кредит успешно погашен!")
            await state.clear()
        else:
            db.close_credit_by_sum(int(msg.text), data["id"])
            await state.clear()
            await msg.answer("Досрочный платеж весен")
    except ValueError:
        await msg.answer("Данные некорректны!")
        await state.clear()

