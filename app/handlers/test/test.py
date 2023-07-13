from pprint import pprint

import requests
from aiogram import Dispatcher, types, Bot
from aiogram.types import InlineKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text

from app.container import plant_service
from app.models.plant import Plant


class DatabaseFilling():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def process_database_filling(self, message: types.Message):
        """Функция наполнения базы данных"""

        import json
        # загружаем файл, созданный парсером с каталогом товаров
        with open('/Users/a/PycharmProjects/bot_fauna3/app/handlers/test/products.jsom') as f:
            json_ = json.load(f)

        # счетчик успешных сохранений
        i = 0

        # счетчик пропущенных с ошибкой сохранений
        skipped = 0

        for item in json_:
            # название категории
            category = list(item.keys())[0]

            title = item.get(category)[0].get('title')
            desc = item.get(category)[0].get('desc')
            price = item.get(category)[0].get('price')

            image = item.get(category)[0].get('image')
            # загружаем фотографию по полученной из каталога ссылке
            photo = requests.get(image)

            # отправляем это фото в чат и сохраняем сообщение в переменную
            msg = await self.bot.send_photo(chat_id=message.chat.id, photo=photo.content)
            # получаем файл ид из сохраненной переменной
            file_id = msg.photo[0].file_id

            try:
                # создаем объект
                obj: Plant = Plant(
                    category=category,
                    name=title.title(),
                    description=desc,
                    price=int(price.replace(" ", "")),
                    photo_id=file_id
                )

                # сохраняем в бд
                plant_service.create_from_obj(obj)

                # выводим текущую задачу
                print(f"{i}. {category} - {title}")

                # увеличиваем счетчик успешных сохранений
                i += 1

            except Exception:
                """при ошибке сохранение (или вероятнее всего преобразования значения price в число) - 
                выводим сообщение об ошибке и увеличиваем счетчик ошибок"""

                print('SKIPPED!!!')
                skipped += 1
                continue

        # выводим общую статистику
        print(f"Сохранено: {i}, Пропущено: {skipped}")


class Test():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def process_test_command(self, message: types.Message):
        items = ['1', '2']

        markup = InlineKeyboardMarkup(resize_keyboard=True)
        buttons = []
        for i, item in enumerate(items):
            button = KeyboardButton(text=f'{item}', callback_data=f'{i + 1}')
            buttons.insert(i, button)
        markup.add(*buttons)

        await message.reply("Reply", reply_markup=markup, reply=False)

    async def process_callback_command(self, call: types.CallbackQuery):

        if call.data == "1":
            await call.message.answer("вы нажали 1")

        if call.data == "2":
            await call.message.answer("вы нажали 2")



def register_test_handlers(dispatcher: Dispatcher):
    # df = DatabaseFilling(dispatcher.bot)
    test = Test(dispatcher.bot)

    # TEST
    commands = ["test"]
    dispatcher.register_message_handler(test.process_test_command, commands=commands, state="*")
    dispatcher.register_callback_query_handler(test.process_callback_command,
                                               (Text(equals=['1', '2'])))
