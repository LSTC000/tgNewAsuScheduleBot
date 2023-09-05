from loader import dp, bot

from data.callbacks import CONFIRM_ALERT_FOR_USERS_CALLBACK_DATA, CANCEL_ALERT_FOR_USERS_CALLBACK_DATA

from data.messages import SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE

from data.redis import ALERT_FOR_USERS_REDIS_KEY

from functions import clear_last_ikb, send_alert, call_admin_menu_ikb

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_ALERT_FOR_USERS_CALLBACK_DATA, CANCEL_ALERT_FOR_USERS_CALLBACK_DATA],
    state=AdminMenuStatesGroup.confirm_alert_for_users
)
async def confirm_alert_for_users(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        text = data[ALERT_FOR_USERS_REDIS_KEY]
        data.pop(ALERT_FOR_USERS_REDIS_KEY)

    if callback.data == CONFIRM_ALERT_FOR_USERS_CALLBACK_DATA:
        # Sending users alert.
        await send_alert(text_alert=text)
        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE)

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call admin menu.
    await call_admin_menu_ikb(user_id=user_id, state=state)
    # Set admin_menu state.
    await AdminMenuStatesGroup.admin_menu.set()
