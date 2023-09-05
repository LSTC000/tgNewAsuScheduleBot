from data.redis import LAST_IKB_REDIS_KEY

from data.messages import HELP_MESSAGE

from keyboards import help_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_help_ikb(user_id: int, state: FSMContext) -> None:
    """call help inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call asu buildings inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=HELP_MESSAGE,
            reply_markup=help_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
