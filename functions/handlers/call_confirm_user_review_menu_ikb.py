from data.redis import LAST_IKB_REDIS_KEY, USER_REVIEW_REDIS_KEY

from data.messages import CONFIRM_USER_REVIEW_MESSAGE

from keyboards import confirm_user_review_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_confirm_user_review_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call confirm user review inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call confirm user review inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=CONFIRM_USER_REVIEW_MESSAGE.format(data[USER_REVIEW_REDIS_KEY]),
            reply_markup=confirm_user_review_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
