from loader import dp

from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE

from data.callbacks import CHAT_GPT_MENU_CALLBACK_DATA

from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from functions import clear_last_ikb, call_chat_gpt_menu_ikb

from states import MainMenuStatesGroup, ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == CHAT_GPT_MENU_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def chat_gpt_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Create empty list for ChatGPT history.
    async with state.proxy() as data:
        data[CHAT_GPT_HISTORY_REDIS_KEY] = [CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE]

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call ChatGPT inline menu.
    await call_chat_gpt_menu_ikb(user_id=user_id, state=state)
    # Set chat_gpt_menu state.
    await ChatGptStatesGroup.chat_gpt_menu.set()
