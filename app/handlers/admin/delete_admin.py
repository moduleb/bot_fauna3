from aiogram import types
from aiogram.dispatcher import FSMContext

from app.container import plant_service

from app.config.messages import MESSAGES
from app.keyboards.admin.admin import get_all_plants_markup, confirm_deletion_markup, admin_markup
from app.states.admin.admin import FSMAdmin

from app.states.admin.delete_admin import FSMDelete

plant_to_delete = []


async def delete_plant(message: types.Message):
    await FSMDelete.choose_plant.set()
    await message.reply("Выбери растение 👇", reply_markup=get_all_plants_markup(), reply=False)


async def confirm_deletion(message: types.Message):
    await FSMDelete.confirm_deletion.set()
    plant_to_delete.append(message.text)
    await message.reply("Подтверждаете удаление?", reply_markup=confirm_deletion_markup)


async def deleted(message: types.Message, state: FSMContext):
    await FSMAdmin.login.set()
    plant_service.delete(plant_to_delete[0])
    plant_to_delete.clear()
    await message.reply("Удалено")
    await message.reply(MESSAGES.admin, reply_markup=admin_markup, reply=False)
