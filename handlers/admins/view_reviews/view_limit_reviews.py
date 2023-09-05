from loader import dp, bot

from data.callbacks import VIEW_LIMIT_REVIEWS_CALLBACK_DATA

from data.messages import ENTER_LIMIT_VIEW_REVIEWS_MESSAGE

from functions import clear_last_ikb

from states import ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == VIEW_LIMIT_REVIEWS_CALLBACK_DATA,
    state=ViewReviewsStatesGroup.view_reviews_menu
)
async def view_limit_reviews(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Enter limit view reviews.
    await bot.send_message(chat_id=user_id, text=ENTER_LIMIT_VIEW_REVIEWS_MESSAGE)
    # Set enter_limit_view_reviews state.
    await ViewReviewsStatesGroup.enter_limit_view_reviews.set()
