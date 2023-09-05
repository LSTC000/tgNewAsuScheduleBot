from loader import dp, bot

from data.callbacks import USER_REVIEW_CALLBACK_DATA

from data.messages import ENTER_USER_REVIEW_MESSAGE

from functions import clear_last_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == USER_REVIEW_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def user_review(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Message about enter user review.
    await bot.send_message(chat_id=user_id, text=ENTER_USER_REVIEW_MESSAGE)
    # Set enter_user_review state.
    await MainMenuStatesGroup.enter_user_review.set()
