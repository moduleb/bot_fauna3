from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.container import plant_service


# ВЫВОД ВООБЩЕ ВСЕХ РАСТЕНИЙ ВКЛЮЧАЯ НЕАКТИВНЫЕ
def get_all_plants_markup():
    active_plants = plant_service.get_all()

    items = ["Назад"]
    for plant in active_plants:
        items.append(plant.name)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i, item in enumerate(items):
        button = KeyboardButton(text=f'{item}', callback_data=f'{i}')
        buttons.insert(i, button)
    markup.add(*buttons)

    return markup


# КНОПКИ В АДМИНКЕ
# items = ["Добавить", "Редактировать", "Удалить"]
items = ["Добавить", "Удалить"]
admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = []
for i, item in enumerate(items):
    button = KeyboardButton(text=f'{item}', callback_data=f'{i}')
    buttons.insert(i, button)
admin_markup.add(*buttons)


# ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ
items = ["Да", "Нет"]

confirm_deletion_markup = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = []
for i, item in enumerate(items):
    button = KeyboardButton(text=f'{item}', callback_data=f'{i}')
    buttons.insert(i, button)
confirm_deletion_markup.add(*buttons)


# ОТМЕНА ПРИ РЕДАКТИРОВАНИИ
i, item = 1, "Отмена"
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text=f'{item}', callback_data=f'{i}')
cancel_markup.add(button)


# РЕДАКТИРОВАНИЕ
def edit_markup(name):
    items = ["Отмена", "Изменить", "Дальше"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i, item in enumerate(items):
        button = KeyboardButton(text=f'{item}', callback_data=f'{i}')
        buttons.insert(i, button)
    markup.add(*buttons)

    return markup
