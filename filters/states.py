from aiogram.fsm.state import State, StatesGroup


class RegistrationCredit(StatesGroup):
    passport_number = State()


class RegistrationCustomer(StatesGroup):
    passport_number = State()


class GetSum(StatesGroup):
    credit_sum = State()


class GeTern(StatesGroup):
    credit_tern = State()


class CreditList(StatesGroup):
    passport_number = State()


class PaymentsList(StatesGroup):
    passport_number = State()


class PaymentsListId(StatesGroup):
    credit_id = State()


class Future(StatesGroup):
    passport_number = State()


class Pay1(StatesGroup):
    passport_number = State()


class Pay2(StatesGroup):
    credit_id = State()

class Pay3(StatesGroup):
    yes_no = State()


class FPay1(StatesGroup):
    passport_number = State()


class FPay2(StatesGroup):
    credit_id = State()


class FPay3(StatesGroup):
    yes_no = State()


class FPay4(StatesGroup):
    fp_sum = State()


class CreditC1(StatesGroup):
    passport_number = State()


class CreditC2(StatesGroup):
    credit_id = State()
