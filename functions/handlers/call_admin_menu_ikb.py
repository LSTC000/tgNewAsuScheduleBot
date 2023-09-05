from data.redis import LAST_IKB_REDIS_KEY

from data.messages import ADMIN_MENU_MESSAGE

from keyboards import admin_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_admin_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call admin inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call admin inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=ADMIN_MENU_MESSAGE,
            reply_markup=admin_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
