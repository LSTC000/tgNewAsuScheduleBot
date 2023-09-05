from data.redis import LAST_IKB_REDIS_KEY

from data.messages import START_COMMAND_MESSAGE

from keyboards import start_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_start_ikb(user_id: int, first_name: str, state: FSMContext) -> None:
    """call start inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        first_name (str): Telegram user first name.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call start inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=START_COMMAND_MESSAGE.format(first_name),
            reply_markup=start_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
