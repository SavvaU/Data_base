import aiogram
import asyncio
from handlers import echo, credit, customer, list_cust
bot = aiogram.Bot(token = "6547940536:AAGURaKzAlAZSrQUVOEO_jmdPIWabCCqyIg")

dp = aiogram.Dispatcher()
dp.include_router(credit.router)
dp.include_router(customer.router)
dp.include_router(list_cust.router)
dp.include_router(echo.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())