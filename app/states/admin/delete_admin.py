from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMDelete(StatesGroup):
    choose_plant = State()
    confirm_deletion = State()
