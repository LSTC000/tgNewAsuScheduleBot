from loader import dp

from data.callbacks import CHAT_GPT_CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from functions import clear_last_ikb, clear_redis_data, call_main_menu_ikb, call_confirm_chat_gpt_clear_history_menu_ikb

from states import MainMenuStatesGroup, ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CHAT_GPT_CANCEL_TO_MAIN_MENU_CALLBACK_DATA,
    state=[ChatGptStatesGroup.chat_gpt_menu]
)
async def chat_gpt_cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        history_length = len(data[CHAT_GPT_HISTORY_REDIS_KEY])

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if history_length > 1:
        # Call confirm ChatGPT clear history inline menu.
        await call_confirm_chat_gpt_clear_history_menu_ikb(user_id=user_id, state=state)
        # Set confirm_chat_gpt_cancel_to_main_menu state.
        await ChatGptStatesGroup.confirm_chat_gpt_cancel_to_main_menu.set()
    else:
        # Clear redis data.
        await clear_redis_data(state=state)
        # Call main inline menu.
        await call_main_menu_ikb(user_id=user_id, state=state)
        # Set main_menu state.
        await MainMenuStatesGroup.main_menu.set()
