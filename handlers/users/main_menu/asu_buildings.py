from loader import dp

from data.callbacks import ASU_BUILDINGS_CALLBACK_DATA

from functions import clear_last_ikb, call_asu_buildings_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == ASU_BUILDINGS_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def asu_buildings(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call asu buildings inline menu.
    await call_asu_buildings_ikb(user_id=user_id, state=state)
    # Set asu_buildings state.
    await MainMenuStatesGroup.asu_buildings.set()
