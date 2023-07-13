from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup

from app.config.messages import MESSAGES
from app.container import user_service
from app.keyboards.admin.admin import admin_markup
from app.keyboards.user.categoties import get_categories_markup
from app.logger import logger
from app.models.user import User
from app.states.admin.admin import FSMAdmin
from app.states.user.catalog import CatalogFSM


# ADMIN
async def process_admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id != 5312665858:
        return
    await FSMAdmin.login.set()
    await message.reply(MESSAGES.admin, reply_markup=admin_markup, reply=False)


# START
async def process_start_command(message: types.Message):
    tg_id = message.from_user.id
    if not user_service.get_one(tg_id):
        user_service.create(tg_id)
    else:
        logger.debug('Создание User в базе данных пропущено, запись уже существует')

    await message.reply(MESSAGES.start, reply_markup=ReplyKeyboardRemove(), reply=False)


# HELP
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES.help, reply_markup=ReplyKeyboardRemove(), reply=False)


# CATALOG
async def process_catalog_command(message: types.Message):
    logger.debug("process_catalog_command")
    await message.reply(MESSAGES.category, reply_markup=get_categories_markup(message.from_user.id), reply=False)
    await CatalogFSM.load_category.set()
    await message.bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup())

async def process_catalog_command_call(call: types.CallbackQuery):
    logger.debug("process_catalog_command")
    await call.message.reply(MESSAGES.category, reply_markup=get_categories_markup(call.from_user.id), reply=False)
    await CatalogFSM.load_category.set()
    await call.message.bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=InlineKeyboardMarkup())



# DEVELOPER
async def process_developer_command(message: types.Message):
    await message.reply(f'{MESSAGES.developer}', reply_markup=ReplyKeyboardRemove(), reply=False)

