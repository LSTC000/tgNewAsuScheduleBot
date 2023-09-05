from loader import dp

from data.callbacks import CANCEL_TO_ADMIN_MENU_CALLBACK_DATA

from functions import clear_last_ikb, clear_redis_data, call_admin_menu_ikb

from states import AdminMenuStatesGroup, ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_ADMIN_MENU_CALLBACK_DATA,
    state=[
        AdminMenuStatesGroup.admin_menu,
        ViewReviewsStatesGroup.view_reviews_menu,
        ViewReviewsStatesGroup.view_review
    ]
)
async def cancel_to_admin_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear redis data.
    await clear_redis_data(state=state)
    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call admin inline menu.
    await call_admin_menu_ikb(user_id=user_id, state=state)
    # Set admin_menu state.
    await AdminMenuStatesGroup.admin_menu.set()
