from loader import dp

from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE

from data.messages import SUCCESSFUL_CHAT_GPT_CLEAR_HISTORY_MESSAGE

from data.callbacks import CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA

from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from functions import clear_last_ikb, clear_redis_data, call_main_menu_ikb, call_chat_gpt_menu_ikb

from states import MainMenuStatesGroup, ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA],
    state=[ChatGptStatesGroup.confirm_chat_gpt_cancel_to_main_menu]
)
async def confirm_chat_gpt_cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if callback.data == CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA:
        await callback.answer(text=SUCCESSFUL_CHAT_GPT_CLEAR_HISTORY_MESSAGE, show_alert=True)

        # Clear redis data.
        await clear_redis_data(state=state)
        # Call main inline menu.
        await call_main_menu_ikb(user_id=user_id, state=state)
        # Set main_menu state.
        await MainMenuStatesGroup.main_menu.set()
    else:
        # Call ChatGPT inline menu.
        await call_chat_gpt_menu_ikb(user_id=user_id, state=state)
        # Set chat_gpt_menu state.
        await ChatGptStatesGroup.chat_gpt_menu.set()
