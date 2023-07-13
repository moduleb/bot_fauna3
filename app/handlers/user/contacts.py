from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove

from app.config.messages import MESSAGES


class ContactsHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def process_contact_handler(self, message: types.Message):
        await self.bot.send_contact(message.chat.id,
                                    first_name=MESSAGES.name,
                                    phone_number=MESSAGES.phone_1,
                                    )

        await message.reply(
            f'{MESSAGES.contacts}',
            reply_markup=ReplyKeyboardRemove(),
            reply=False,
            disable_notification=True)
