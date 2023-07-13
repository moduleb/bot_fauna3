from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMUpload(StatesGroup):
    photo = State()
    name = State()
    description = State()
    category = State()
    price = State()