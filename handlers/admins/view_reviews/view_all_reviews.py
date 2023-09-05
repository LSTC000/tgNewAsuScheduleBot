from loader import dp, bot

from data.callbacks import VIEW_ALL_REVIEWS_CALLBACK_DATA

from data.messages import ERROR_VIEW_ALL_REVIEWS_MESSAGE

from data.redis import COUNT_REVIEWS_REDIS_KEY

from functions import clear_last_ikb, call_view_reviews_menu_ikb, call_view_review_ikb

from states import ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == VIEW_ALL_REVIEWS_CALLBACK_DATA,
    state=ViewReviewsStatesGroup.view_reviews_menu
)
async def view_all_reviews(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        count_reviews = int(data[COUNT_REVIEWS_REDIS_KEY])

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if count_reviews < 1:
        # Enter limit view reviews.
        await bot.send_message(chat_id=user_id, text=ERROR_VIEW_ALL_REVIEWS_MESSAGE)
        # Call view reviews menu.
        await call_view_reviews_menu_ikb(user_id=user_id, state=state)
        # Set view_reviews_menu state.
        await ViewReviewsStatesGroup.view_reviews_menu.set()
    else:
        # Call view review menu.
        await call_view_review_ikb(user_id=user_id, state=state)
        # Set view_review state.
        await ViewReviewsStatesGroup.view_review.set()
