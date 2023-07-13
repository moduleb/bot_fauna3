from aiogram import types, Bot
from aiogram.dispatcher import FSMContext

from app.container import plant_service
from app.keyboards.admin import cancel_markup, admin_markup, edit_markup
from app.config.messages import MESSAGES
from app.states.admin import FSMAdmin
from app.states.admin.edit_admin import FSMEdit

class EditAdmin:
    
    def __init__(self, bot: Bot):
        self.bot = bot
        
    async def edit(self, message: types.Message):
        await FSMEdit.photo.set()
        plant = plant_service.get_one(message.text)
        await self.bot.send_photo(message.chat.id, plant.photo_id)
        await message.reply("Выбери действие", reply_markup=edit_markup())
    
    
    async def load_photo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo_id'] = message.photo[0].file_id
        await FSMEdit.next()
        await message.reply("Выбери действие", reply_markup=edit_markup())
    
    
    async def load_name(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMEdit.next()
        await message.reply("Введи описание", reply_markup=cancel_markup)
    
    
    async def load_description(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['description'] = message.text
        # await FSMEdit.next()
        # await message.reply("Теперь укажи категорию", reply_markup=ReplyKeyboardRemove())
        plant_service.create(data)
        await message.reply("Запись создана", reply=False)
        await message.reply(MESSAGES.admin, reply_markup=admin_markup, reply=False)
        await FSMAdmin.login.set()
    
    
    # async def load_category(self, message: types.Message, state: FSMContext):
    #     async with state.proxy() as data:
    #         data['category'] = message.text
    #     await FSMEdit.next()
    #     await message.reply("Теперь укажи цену", reply_markup=cancel_markup)
    #
    #
    # async def load_price(self, message: types.Message, state: FSMContext):
    #     async with state.proxy() as data:
    #         data['price'] = int(message.text)
    #     plant_service.create(data)
    #     await message.reply("Запись создана")
    #     await FSMAdmin.login.set()
