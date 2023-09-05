from loader import dp

from data.callbacks import CHANGE_USER_ALERT_CALLBACK_DATA

from functions import edit_main_menu_ikb, UserInfoCache

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == CHANGE_USER_ALERT_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def change_user_alert(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    user_info = UserInfoCache(user_id)
    # Update user alert.
    await user_info.update_user_alert_cache(alert=not(await user_info.get_user_alert_cache()))
    # Edit alert in the main inline keyboard menu.
    await edit_main_menu_ikb(user_id=user_id, state=state)
