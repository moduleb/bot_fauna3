from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from app.handlers.user import contacts
from app.handlers.user.catalog import CatalogHandler
from app.handlers.user.common import process_start_command, process_help_command, process_catalog_command, \
    process_catalog_command_call
from app.handlers.user.favourites import FavouritesHandler
from app.states.user.catalog import CatalogFSM



def register_user_handlers(dispatcher: Dispatcher):
    catalog_handler = CatalogHandler(dispatcher.bot)
    favourites_handler = FavouritesHandler(dispatcher.bot)

    # регистрация callback inline кнопки нразад
    dispatcher.register_callback_query_handler(process_catalog_command_call,
                                               lambda call: call.data == '0', state=CatalogFSM.load_plant)

    dispatcher.register_callback_query_handler(catalog_handler.process_like_command_call,
                                               text_startswith="like", state=CatalogFSM.load_plant)

    dispatcher.register_callback_query_handler(catalog_handler.process_dislike_command_call,
                                               text_startswith="dislike", state=CatalogFSM.load_plant)

    # регистрация callback inline кнопок предыдущий и следующий
    dispatcher.register_callback_query_handler(catalog_handler.plant_click_handler_call,
                                               text_startswith="name", state=CatalogFSM.load_plant)


    # FAVOURITES
    commands = ["favourites"]
    dispatcher.register_message_handler(favourites_handler.process_favourites, commands=commands, state="*")
    dispatcher.register_message_handler(favourites_handler.process_favourites, Text(equals=commands, ignore_case=True), state="*")

    # START
    commands = ["start", "старт", "начать", "запуск", "запустить"]
    dispatcher.register_message_handler(process_start_command, commands=commands, state="*")
    dispatcher.register_message_handler(process_start_command, Text(equals=commands, ignore_case=True), state="*")

    # CONTACTS
    commands = ["contacts", "контакты", "адрес", "телефон", "режим работы"]
    contacts_handler = contacts.ContactsHandler(dispatcher.bot)
    dispatcher.register_message_handler(contacts_handler.process_contact_handler,
                                        Text(equals=commands, ignore_case=True), state="*")
    dispatcher.register_message_handler(contacts_handler.process_contact_handler, commands=commands, state="*")

    # HELP
    commands = ["help", "помощь", "справка", "команды"]
    dispatcher.register_message_handler(process_help_command, commands=commands, state="*")
    dispatcher.register_message_handler(process_help_command, Text(equals=commands, ignore_case=True), state="*")

    # DEVELOPER
    # commands = ["developer", "разработчик"]
    # dispatcher.register_message_handler(process_developer_command, commands=commands, state="*")
    # dispatcher.register_message_handler(process_developer_command, Text(equals=commands, ignore_case=True), state="*")

    # CATALOG
    commands = ["catalog", "каталог", "товары"]
    dispatcher.register_message_handler(process_catalog_command, commands=commands, state="*")
    dispatcher.register_message_handler(process_catalog_command, Text(equals=commands, ignore_case=True), state="*")

    # выбор favourites
    dispatcher.register_message_handler(catalog_handler.process_favourites, Text(equals='❤️ Избранное'),
                                        state=CatalogFSM.load_category)
    # выбор категории
    dispatcher.register_message_handler(catalog_handler.category_click_handler,
                                        state=CatalogFSM.load_category)
    # назад при выборе растения
    dispatcher.register_message_handler(process_catalog_command, Text(equals="назад", ignore_case=True),
                                        state=CatalogFSM.load_plant)

    # выбор растения
    dispatcher.register_message_handler(catalog_handler.plant_click_handler,
                                        state=CatalogFSM.load_plant)

