from loader import dp

from data.config import ADMINS

from functions import clear_last_ikb, call_admin_menu_ikb

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['admin'], state='*')
async def admin_cmd(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in ADMINS:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)
        # Call admin menu.
        await call_admin_menu_ikb(user_id=user_id, state=state)
        # Set admin_menu state.
        await AdminMenuStatesGroup.admin_menu.set()
