from loader import dp

from data.callbacks import VIEW_REVIEWS_MENU_CALLBACK_DATA

from functions import clear_last_ikb, call_view_reviews_menu_ikb

from states import AdminMenuStatesGroup, ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == VIEW_REVIEWS_MENU_CALLBACK_DATA, state=AdminMenuStatesGroup.admin_menu)
async def view_reviews_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call view reviews inline keyboard menu.
    await call_view_reviews_menu_ikb(user_id=user_id, state=state)
    # Set view_reviews_menu state.
    await ViewReviewsStatesGroup.view_reviews_menu.set()
