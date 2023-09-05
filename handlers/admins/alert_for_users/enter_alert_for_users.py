from loader import dp, bot

from data.messages import ERROR_ALERT_FOR_USERS_MESSAGE

from data.redis import ALERT_FOR_USERS_REDIS_KEY

from functions import clear_last_ikb, call_admin_menu_ikb, call_confirm_alert_for_users_menu_ikb

from utils import Validator

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.enter_alert_for_users)
async def enter_alert_for_users(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Check alert on valid.
    if Validator().alert_validation(text):
        async with state.proxy() as data:
            data[ALERT_FOR_USERS_REDIS_KEY] = text
        # Call confirm menu.
        await call_confirm_alert_for_users_menu_ikb(user_id=user_id, state=state)
        # Set confirm_alert_for_users state.
        await AdminMenuStatesGroup.confirm_alert_for_users.set()
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_ALERT_FOR_USERS_MESSAGE)
        # Call admin menu.
        await call_admin_menu_ikb(user_id=user_id, state=state)
        # Set admin_menu state.
        await AdminMenuStatesGroup.admin_menu.set()
