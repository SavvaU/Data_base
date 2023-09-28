import aiogram
import asyncio
from handlers import credit, customer, list_cust, list_credit, fee, payments_list, pay, futurepayment, credit_check, polis_blank, finanse, menu, clear
bot = aiogram.Bot(token="6547940536:AAGURaKzAlAZSrQUVOEO_jmdPIWabCCqyIg")

dp = aiogram.Dispatcher()
dp.include_router(credit.router)
dp.include_router(customer.router)
dp.include_router(list_cust.router)
dp.include_router(list_credit.router)
dp.include_router(fee.router)
dp.include_router(payments_list.router)
dp.include_router(pay.router)
dp.include_router(futurepayment.router)
dp.include_router(credit_check.router)
dp.include_router(polis_blank.router)
dp.include_router(finanse.router)
dp.include_router(menu.router)
dp.include_router(clear.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())