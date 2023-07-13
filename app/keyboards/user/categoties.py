from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.container import plant_service, user_service


def get_categories_markup(user_tg_id):

    # создаем markup
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []

    # получаем все категории из бд
    categories = plant_service.get_all_categories()

    user = user_service.get_one(user_tg_id)

    likes = user_service.get_all(user.id)

    if likes:
        # создаем кнопку избранное и добавляем в markup
        button = KeyboardButton(text=f'❤️ Избранное', callback_data='favourites')
        buttons.append(button)

    for category in categories:
        button = KeyboardButton(text=f'{category[0]}', callback_data=f'cat_{category[0]}')
        buttons.append(button)
    markup.add(*buttons)

    return markup
