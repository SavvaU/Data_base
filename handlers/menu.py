from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from database.db import create_db
from aiogram.fsm.context import FSMContext


router = Router()
db = create_db()


@router.message(Command(commands="menu"))
async def menu(msg: Message, state=FSMContext):
    out = "Меню: \n/credit - выдача кредита.\n/pay - внесение платежа.\n/credit_check - проверка наличия платежей.\n/fpay - досрочное погашение.\n/reg - регистрация клиента.\n/fee - начисление пени.\n/fin - отчет за год\n/credit_list - лист кредитов.\n/cust_list - список клиентов.\n/payments_list - писок платежей.\n/polis - повестки в суд.\n/clear - очистка состояний."
    await msg.answer(out)