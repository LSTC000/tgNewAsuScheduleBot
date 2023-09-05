from loader import dp, bot

from data.messages import ERROR_ENTER_USER_REVIEW_MESSAGE

from data.redis import USER_REVIEW_REDIS_KEY

from functions import call_main_menu_ikb, call_confirm_user_review_menu_ikb

from states import MainMenuStatesGroup

from utils import Validator

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(state=MainMenuStatesGroup.enter_user_review)
async def enter_user_review(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text

    # Check review on valid
    if Validator().user_review_validation(text):
        async with state.proxy() as data:
            data[USER_REVIEW_REDIS_KEY] = text
        # Call confirm user review inline keyboard.
        await call_confirm_user_review_menu_ikb(user_id=user_id, state=state)
        # Set enter_user_review state.
        await MainMenuStatesGroup.confirm_user_review.set()
    else:
        # Inform the user about an error when entering the review.
        await bot.send_message(chat_id=user_id, text=ERROR_ENTER_USER_REVIEW_MESSAGE)
        # Call main inline menu.
        await call_main_menu_ikb(user_id=user_id, state=state)
        # Set main_menu state.
        await MainMenuStatesGroup.main_menu.set()
        