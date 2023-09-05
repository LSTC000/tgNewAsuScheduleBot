from data.redis import LAST_IKB_REDIS_KEY, ALERT_FOR_USERS_REDIS_KEY

from data.messages import CONFIRM_ALERT_FOR_USERS_MESSAGE

from keyboards import confirm_alert_for_users_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_confirm_alert_for_users_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call confirm alert for users inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call confirm alert for users inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=CONFIRM_ALERT_FOR_USERS_MESSAGE.format(data[ALERT_FOR_USERS_REDIS_KEY]),
            reply_markup=confirm_alert_for_users_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
