from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatGptStatesGroup(StatesGroup):
    chat_gpt_menu = State()
    confirm_chat_gpt_clear_history = State()
    confirm_chat_gpt_cancel_to_main_menu = State()
