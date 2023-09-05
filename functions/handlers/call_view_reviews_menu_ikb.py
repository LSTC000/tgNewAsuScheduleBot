from data.redis import LAST_IKB_REDIS_KEY, COUNT_REVIEWS_REDIS_KEY

from data.messages import VIEW_REVIEWS_MENU_MESSAGE

from database import get_count_reviews

from keyboards import view_reviews_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_view_reviews_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call view reviews inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        if COUNT_REVIEWS_REDIS_KEY not in data:
            data[COUNT_REVIEWS_REDIS_KEY] = await get_count_reviews()
        # Call view reviews inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=VIEW_REVIEWS_MENU_MESSAGE.format(data[COUNT_REVIEWS_REDIS_KEY]),
            reply_markup=view_reviews_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
