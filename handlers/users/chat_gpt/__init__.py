__all__ = ['register_users_chat_gpt']


from .chat_gpt_menu import chat_gpt_menu
from .chat_gpt_clear_history import chat_gpt_clear_history
from .confirm_chat_gpt_clear_history import confirm_chat_gpt_clear_history
from .chat_gpt_response import chat_gpt_response

from aiogram import Dispatcher


def register_users_chat_gpt(dp: Dispatcher):
    dp.register_callback_query_handler(chat_gpt_menu)
    dp.register_callback_query_handler(chat_gpt_clear_history)
    dp.register_callback_query_handler(confirm_chat_gpt_clear_history)
    dp.register_message_handler(chat_gpt_response)
