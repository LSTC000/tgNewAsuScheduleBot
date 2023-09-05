from loader import dp

from data.callbacks import SOCIAL_CALLBACK_DATA

from functions import clear_last_ikb, call_social_ikb

from states import MainMenuStatesGroup, SocialStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == SOCIAL_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def social_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call social inline menu.
    await call_social_ikb(user_id=user_id, state=state)
    # Set social_menu state.
    await SocialStatesGroup.social_menu.set()
