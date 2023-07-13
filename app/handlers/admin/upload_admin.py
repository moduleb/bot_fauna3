from aiogram import types
from aiogram.dispatcher import FSMContext

from app.config.messages import MESSAGES
from app.container import plant_service
from app.keyboards.admin.admin import cancel_markup, admin_markup
from app.states.admin.admin import FSMAdmin
from app.states.admin.upload_admin import FSMUpload


async def upload(message: types.Message):
    await FSMUpload.photo.set()
    await message.reply("Загрузи фото", reply_markup=cancel_markup, reply=False)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo_id'] = message.photo[0].file_id
    await FSMUpload.next()
    await message.reply("Теперь введи название", reply_markup=cancel_markup, reply=False)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMUpload.next()
    await message.reply("Введи описание", reply_markup=cancel_markup, reply=False)


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMUpload.next()
    await message.reply("Теперь укажи категорию", reply_markup=cancel_markup, reply=False)



async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMUpload.next()
    await message.reply("Теперь укажи цену (только цифры)", reply_markup=cancel_markup, reply=False)


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
    plant_service.create(data)
    await message.reply("Запись создана", reply=False)
    await message.reply(MESSAGES.admin, reply_markup=admin_markup, reply=False)
    await FSMAdmin.login.set()
