__all__ = ['register_users_cancels']


from .cancel_to_main_menu import cancel_to_main_menu
from .cancel_to_schedule_menu import cancel_to_schedule_menu
from .chat_gpt_cancel_to_main_menu import chat_gpt_cancel_to_main_menu
from .confirm_chat_gpt_cancel_to_main_menu import confirm_chat_gpt_cancel_to_main_menu

from aiogram import Dispatcher


def register_users_cancels(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_to_main_menu)
    dp.register_callback_query_handler(cancel_to_schedule_menu)
    dp.register_callback_query_handler(chat_gpt_cancel_to_main_menu)
    dp.register_callback_query_handler(confirm_chat_gpt_cancel_to_main_menu)
