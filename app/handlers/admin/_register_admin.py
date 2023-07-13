from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from app.handlers.admin.delete_admin import delete_plant, confirm_deletion, deleted
from app.handlers.admin.upload_admin import upload, load_photo, load_name, load_description, load_category, load_price
from app.handlers.user.common import process_admin_command
from app.logger import logger
from app.states.admin.admin import FSMAdmin
from app.states.admin.delete_admin import FSMDelete
from app.states.admin.upload_admin import FSMUpload


def register_admin_handlers(dispatcher: Dispatcher):

    # ADMIN
    dispatcher.register_message_handler(process_admin_command, commands=["admin"], state="*")

    # UPLOAD
    dispatcher.register_message_handler(upload, Text(equals='Добавить'), state=FSMAdmin.login)
    dispatcher.register_message_handler(process_admin_command, Text(equals='Отмена'), state=FSMUpload.all_states)
    dispatcher.register_message_handler(load_photo, content_types=['photo'], state=FSMUpload.photo)
    dispatcher.register_message_handler(load_name, state=FSMUpload.name)
    dispatcher.register_message_handler(load_description, state=FSMUpload.description)
    dispatcher.register_message_handler(load_category, state=FSMUpload.category)
    dispatcher.register_message_handler(load_price, state=FSMUpload.price)

    # DELETE
    dispatcher.register_message_handler(delete_plant, Text(equals='Удалить'), state=FSMAdmin.login)
    dispatcher.register_message_handler(process_admin_command, Text(equals='Назад'), state=FSMDelete.choose_plant)
    dispatcher.register_message_handler(confirm_deletion, state=FSMDelete.choose_plant)
    dispatcher.register_message_handler(deleted, Text(equals='Да'), state=FSMDelete.confirm_deletion)
    dispatcher.register_message_handler(process_admin_command, Text(equals='Нет'), state=FSMDelete.confirm_deletion)