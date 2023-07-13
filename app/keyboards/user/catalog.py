from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

from app.container import plant_service, user_service
from app.logger import logger


def get_active_plants_markup(active_plants):
    logger.debug('get_active_plants_markup')

    buttons = []

    for i, plant in enumerate(active_plants):
        button = KeyboardButton(text=plant, callback_data=str(i))
        buttons.insert(i, button)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button = KeyboardButton(text="Назад", callback_data='0')
    buttons.insert(1000, button)

    markup.add(*buttons)

    return markup


def prev_next_inline_markup(user_tg_id, current_plant, active_plants, liked=None):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = []

    button = KeyboardButton(text='📚', callback_data="0")
    buttons.insert(1, button)


    if liked is None:
        plant_id = plant_service.get_one(current_plant).id
        user = user_service.get_one(user_tg_id)
        if not user:
            user_service.create(user_tg_id)
        user = user_service.get_one(user_tg_id)


        logger.debug(f"liked: None, plant_id: {plant_id}, user_id: {user.id}")
        like_obj = user_service.check_like(user.id, plant_id)
        logger.debug(f'Найден объект: {like_obj}')
        if like_obj:
            liked = True


    if liked:
        button = KeyboardButton(text='❤️', callback_data=f"dislike_{current_plant}")
    else:
        button = KeyboardButton(text='🤍', callback_data=f"like_{current_plant}")

    buttons.insert(2, button)




    logger.debug(f'current_plant_name: {current_plant}')
    current_plant_number = active_plants.index(current_plant)

    prev = current_plant_number - 1
    if prev >= 0:
        button = KeyboardButton(text='◀️', callback_data=f'name_{active_plants[prev]}')
        buttons.insert(3, button)

    next = current_plant_number + 1
    if next < len(active_plants):
        button = KeyboardButton(text='▶️', callback_data=f'name_{active_plants[next]}')
        buttons.insert(4, button)

    markup.add(*buttons)
    logger.debug(f'prev: {prev}, current: {current_plant_number}, next: {next}, length: {len(active_plants)}')

    return markup
