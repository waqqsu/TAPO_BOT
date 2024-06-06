import asyncio
from aiogram import Bot, Dispatcher

from hackaton.handler import router

async def main():
    bot=Bot(token='6487097476:AAHEmrv6CGvhZpk8-RWhp5MmlHaTNWas7ps')
    dp=Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop Bot')
