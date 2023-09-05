__all__ = ['register_users_reviews']


from .user_review import user_review
from .enter_user_review import enter_user_review
from .confirm_user_review import confirm_user_review

from aiogram import Dispatcher


def register_users_reviews(dp: Dispatcher):
    dp.register_callback_query_handler(user_review)
    dp.register_message_handler(enter_user_review)
    dp.register_callback_query_handler(confirm_user_review)
