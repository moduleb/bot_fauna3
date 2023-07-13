from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup

from app.config.messages import MESSAGES
from app.container import plant_service, user_service
from app.keyboards.user.catalog import get_active_plants_markup, prev_next_inline_markup
from app.logger import logger
from app.models.plant import Plant
from app.models.user import User
from app.states.user.catalog import CatalogFSM

active_plants = []


class CatalogHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def process_favourites(self, message: types.Message):
        logger.debug("process_favourites")
        global active_plants
        user = user_service.get_one(message.from_user.id)
        likes = user_service.get_all(user_id=user.id)
        global active_plants
        liked_plants = []
        for like in likes:
            plant = plant_service.get_one_by_id(like.plant_id)
            liked_plants.append(plant.name)
        active_plants = liked_plants
        await message.reply(
            MESSAGES.catalog,
            reply_markup=get_active_plants_markup(active_plants),
            reply=False)
        await CatalogFSM.load_plant.set()

    async def category_click_handler(self, message: types.Message):
        logger.debug("category_click_handler")
        category = message.text
        global active_plants
        active_plants = [plant.name for plant in plant_service.get_all_active_by_category(category)]
        await message.reply(MESSAGES.catalog, reply_markup=get_active_plants_markup(active_plants),
                            reply=False)

        await CatalogFSM.load_plant.set()

    async def plant_click_handler(self, message: types.Message):
        user_tg_id = message.from_user.id
        logger.debug("plant_click_handler")

        plant = plant_service.get_one(message.text)
        await self.bot.send_photo(
            chat_id=message.chat.id,
            photo=plant.photo_id,
            caption=f'{plant.name}\n'
                    f'{plant.description}\n\nЦена: {plant.price} рублей.',
            reply_markup=prev_next_inline_markup(user_tg_id,
                                                 message.text,
                                                 active_plants)
        )
        await message.bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=InlineKeyboardMarkup())

    async def plant_click_handler_call(self, call: types.CallbackQuery):
        logger.debug("plant_click_handler_call")
        user_tg_id = call.from_user.id
        name = call.data.split("_")[1]
        plant = plant_service.get_one(name)
        current_plant = name
        await self.bot.send_photo(
            chat_id=call.message.chat.id,
            photo=plant.photo_id,
            caption=f'{plant.name}\n'
                    f'{plant.description}\n\nЦена: {plant.price} рублей.',
            reply_markup=prev_next_inline_markup(user_tg_id,
                                                 current_plant,
                                                 active_plants)
        )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=InlineKeyboardMarkup())

    async def process_like_command_call(self, call: types.CallbackQuery):
        logger.debug("process_like_command_call")
        plant_name = call.data.split("_")[1]
        plant_obj: Plant = plant_service.get_one(plant_name)
        plant_id = plant_obj.id
        user_tg_id = call.from_user.id
        user_obj: User = user_service.get_one(tg_id=user_tg_id)
        user_id = user_obj.id
        user_service.like(user_id=user_id, plant_id=plant_id)
        await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                 message_id=call.message.message_id,
                                                 reply_markup=prev_next_inline_markup(
                                                     user_tg_id, plant_name, active_plants, liked=True))

    async def process_dislike_command_call(self, call: types.CallbackQuery):
        logger.debug("process_like_command_call")
        plant_name = call.data.split("_")[1]
        plant_obj: Plant = plant_service.get_one(plant_name)
        plant_id = plant_obj.id
        user_tg_id = call.from_user.id
        user_obj: User = user_service.get_one(tg_id=user_tg_id)
        user_id = user_obj.id
        user_service.dislike(user_id=user_id, plant_id=plant_id)

        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=prev_next_inline_markup(
                user_tg_id, plant_name, active_plants, liked=False))
