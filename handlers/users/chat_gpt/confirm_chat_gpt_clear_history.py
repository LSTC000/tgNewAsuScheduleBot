from loader import dp

from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE

from data.callbacks import CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA

from data.messages import SUCCESSFUL_CHAT_GPT_CLEAR_HISTORY_MESSAGE

from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from functions import clear_last_ikb, call_chat_gpt_menu_ikb

from states import ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA],
    state=ChatGptStatesGroup.confirm_chat_gpt_clear_history
)
async def confirm_chat_gpt_clear_history(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    if callback.data == CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA:
        async with state.proxy() as data:
            data[CHAT_GPT_HISTORY_REDIS_KEY].clear()
            data[CHAT_GPT_HISTORY_REDIS_KEY].append(CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE)

        await callback.answer(text=SUCCESSFUL_CHAT_GPT_CLEAR_HISTORY_MESSAGE, show_alert=True)

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call ChatGPT inline menu.
    await call_chat_gpt_menu_ikb(user_id=user_id, state=state)
    # Set chat_gpt_menu state.
    await ChatGptStatesGroup.chat_gpt_menu.set()
