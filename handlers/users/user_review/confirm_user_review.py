from loader import dp, bot

from data.callbacks import CONFIRM_USER_REVIEW_CALLBACK_DATA, CANCEL_USER_REVIEW_CALLBACK_DATA

from data.messages import SUCCESSFUL_ENTER_USER_REVIEW_MESSAGE

from data.redis import USER_REVIEW_REDIS_KEY

from database import add_user_review

from functions import clear_last_ikb, call_main_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_USER_REVIEW_CALLBACK_DATA, CANCEL_USER_REVIEW_CALLBACK_DATA], 
    state=MainMenuStatesGroup.confirm_user_review
)
async def confirm_user_review(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        text = data[USER_REVIEW_REDIS_KEY]
        data.pop(USER_REVIEW_REDIS_KEY)

    if callback.data == CONFIRM_USER_REVIEW_CALLBACK_DATA:
        # Add user review in database.
        await add_user_review(user_id=user_id, review=text)
        # Inform the user about a successful adding the review.
        await bot.send_message(chat_id=user_id, text=SUCCESSFUL_ENTER_USER_REVIEW_MESSAGE)

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call admin menu.
    await call_main_menu_ikb(user_id=user_id, state=state)
    # Set main_menu state.
    await MainMenuStatesGroup.main_menu.set()
