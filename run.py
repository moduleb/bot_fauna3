import asyncio

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from app.config import config
from app.config.commands import commands
from app.handlers.admin import _register_admin
from app.handlers.user import _register_user
from app.handlers.test import test
from app.logger import logger
from app.middlewares.logger import LoggingMiddleware


async def main():

    # Форматирование логгера
    # logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
    #                     level=logging.DEBUG)

    # Создаем бота
    bot = Bot(token=config.config.token.TOKEN, parse_mode=types.ParseMode.HTML)
    dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())

    # Регистрация хендлеров
    _register_admin.register_admin_handlers(dispatcher)
    _register_user.register_user_handlers(dispatcher)
    test.register_test_handlers(dispatcher)

    # Регистрация middlewares
    dispatcher.middleware.setup(LoggingMiddleware())
    # dispatcher.middleware.setup(ThrottlingMiddleware())

    # Устанавливаем отображаемые команды
    commands_set = [BotCommand(command, description) for command, description in commands.items()]
    await bot.set_my_commands(commands_set)


    # Запуск поллинга
    try:
        logger.info("Bot started...")
        await dispatcher.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
        await dispatcher.start_polling(bot)

    finally:
        s = await bot.get_session()
        await s.close()
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
