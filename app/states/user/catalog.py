from aiogram.dispatcher.filters.state import StatesGroup, State


class CatalogFSM(StatesGroup):
    load_category = State()
    load_plant = State()