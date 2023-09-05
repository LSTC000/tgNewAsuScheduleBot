from data.redis import LAST_IKB_REDIS_KEY

from data.messages import ASU_BUILDINGS_LOCATION_MESSAGE

from keyboards import asu_buildings_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_asu_buildings_ikb(user_id: int, state: FSMContext) -> None:
    """call asu buildings inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call asu buildings inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=ASU_BUILDINGS_LOCATION_MESSAGE,
            reply_markup=asu_buildings_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
