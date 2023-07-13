from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove

from app.config.messages import MESSAGES
from app.container import user_service, plant_service
from app.keyboards.user.catalog import get_active_plants_markup
from app.logger import logger
from app.states.user.catalog import CatalogFSM


class FavouritesHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def process_favourites(self, message: types.Message):
        logger.debug("process_favourites")
        global active_plants
        user = user_service.get_one(message.from_user.id)
        likes = user_service.get_all(user_id=user.id)
        active_plants.clear()
        for like in likes:
            plant = plant_service.get_one_by_id(like.plant_id)
            active_plants.append(plant.name)
        await message.reply(
            MESSAGES.catalog,
            reply_markup=get_active_plants_markup(active_plants),
            reply=False)
        await CatalogFSM.load_plant.set()

        # user = user_service.get_one(message.from_user.id)
        # likes = user_service.get_all(user.id)
        # for like in likes:
        #     plant = plant_service.get_one_by_id(like.plant_id)
        #     await message.reply(plant.name, reply_markup=ReplyKeyboardRemove(), reply=False)
