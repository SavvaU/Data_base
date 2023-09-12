from aiogram.fsm.state import State, StatesGroup


class RegistrationCredit(StatesGroup):
    passport_number = State()


class RegistrationCustomer(StatesGroup):
    passport_number = State()


class GetSum(StatesGroup):
    credit_sum = State()
