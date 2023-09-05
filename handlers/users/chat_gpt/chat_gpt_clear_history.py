from loader import dp

from data.callbacks import CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA

from data.messages import EMPTY_CHAT_GPT_HISTORY_MESSAGE

from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from functions import clear_last_ikb, call_confirm_chat_gpt_clear_history_menu_ikb

from states import ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA,
    state=ChatGptStatesGroup.chat_gpt_menu
)
async def chat_gpt_clear_history(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        history = data[CHAT_GPT_HISTORY_REDIS_KEY]

    if len(history) > 1:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)
        # Call confirm ChatGPT clear history inline menu.
        await call_confirm_chat_gpt_clear_history_menu_ikb(user_id=user_id, state=state)
        # Set confirm_chat_gpt_clear_history state.
        await ChatGptStatesGroup.confirm_chat_gpt_clear_history.set()
    else:
        await callback.answer(text=EMPTY_CHAT_GPT_HISTORY_MESSAGE, show_alert=True)
