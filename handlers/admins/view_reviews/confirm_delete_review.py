from loader import dp, bot

from data.callbacks import CONFIRM_DELETE_REVIEW_CALLBACK_DATA, CANCEL_DELETE_REVIEW_CALLBACK_DATA

from data.messages import SUCCESSFUL_DELETE_REVIEW_MESSAGE, NOT_FOUND_REVIEWS_MESSAGE

from data.redis import COUNT_REVIEWS_REDIS_KEY, REVIEW_NUMBER_REDIS_KEY, REVIEWS_DATA_REDIS_KEY

from database import delete_review

from functions import clear_last_ikb, clear_redis_data, call_view_review_ikb, call_admin_menu_ikb

from states import AdminMenuStatesGroup, ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_DELETE_REVIEW_CALLBACK_DATA, CANCEL_DELETE_REVIEW_CALLBACK_DATA],
    state=ViewReviewsStatesGroup.confirm_delete_review
)
async def confirm_delete_review(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    callback_data = callback.data

    if callback_data == CONFIRM_DELETE_REVIEW_CALLBACK_DATA:
        async with state.proxy() as data:
            review_number = int(data[REVIEW_NUMBER_REDIS_KEY])
            count_review = int(data[COUNT_REVIEWS_REDIS_KEY])
            reviews_data = data[REVIEWS_DATA_REDIS_KEY]

            await delete_review(review_id=reviews_data[review_number][0])

            count_review -= 1
            data[COUNT_REVIEWS_REDIS_KEY] = count_review
            data[REVIEW_NUMBER_REDIS_KEY] = review_number - 1 if review_number > 0 else review_number
            data[REVIEWS_DATA_REDIS_KEY].pop(review_number)

            await callback.answer(text=SUCCESSFUL_DELETE_REVIEW_MESSAGE, show_alert=True)

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if callback_data == CANCEL_DELETE_REVIEW_CALLBACK_DATA or count_review:
        # Call view review inline keyboard menu.
        await call_view_review_ikb(user_id=user_id, state=state, callback_data=None)
        # Set view_review state.
        await ViewReviewsStatesGroup.view_review.set()
    else:
        await bot.send_message(chat_id=user_id, text=NOT_FOUND_REVIEWS_MESSAGE)

        # Clear redis data.
        await clear_redis_data(state=state)
        # Call admin inline keyboard menu.
        await call_admin_menu_ikb(user_id=user_id, state=state)
        # Set admin_menu state.
        await AdminMenuStatesGroup.admin_menu.set()
