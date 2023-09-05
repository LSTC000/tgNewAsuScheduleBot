from loader import dp

from data.callbacks import PREV_REVIEW_CALLBACK_DATA, NEXT_REVIEW_CALLBACK_DATA, DELETE_REVIEW_CALLBACK_DATA

from functions import clear_last_ikb, call_view_review_ikb

from states import ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [PREV_REVIEW_CALLBACK_DATA, NEXT_REVIEW_CALLBACK_DATA, DELETE_REVIEW_CALLBACK_DATA],
    state=ViewReviewsStatesGroup.view_review
)
async def view_review(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    callback_data = callback.data

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if callback_data == DELETE_REVIEW_CALLBACK_DATA:
        # Set confirm_delete_review state.
        await ViewReviewsStatesGroup.confirm_delete_review.set()

    # Call view review inline keyboard menu.
    await call_view_review_ikb(user_id=user_id, state=state, callback_data=callback_data)
