from data.redis import LAST_IKB_REDIS_KEY

from data.messages import SCHEDULE_MENU_MESSAGE

from keyboards import schedule_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_schedule_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call schedule inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call schedule inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=SCHEDULE_MENU_MESSAGE,
            reply_markup=schedule_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
