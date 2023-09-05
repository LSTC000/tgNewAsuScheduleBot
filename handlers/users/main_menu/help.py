from loader import dp

from data.callbacks import HELP_CALLBACK_DATA

from functions import clear_last_ikb, call_help_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == HELP_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def help(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call help inline menu.
    await call_help_ikb(user_id=user_id, state=state)
    # Set help state.
    await MainMenuStatesGroup.help.set()
