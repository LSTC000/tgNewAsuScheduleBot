__all__ = ['register_admins_view_reviews']


from .view_reviews_menu import view_reviews_menu
from .view_all_reviews import view_all_reviews
from .view_limit_reviews import view_limit_reviews
from .enter_limit_view_reviews import enter_limit_view_reviews
from .view_review import view_review
from .confirm_delete_review import confirm_delete_review

from aiogram import Dispatcher


def register_admins_view_reviews(dp: Dispatcher):
    dp.register_callback_query_handler(view_reviews_menu)
    dp.register_callback_query_handler(view_all_reviews)
    dp.register_callback_query_handler(view_limit_reviews)
    dp.register_message_handler(enter_limit_view_reviews)
    dp.register_callback_query_handler(view_review)
    dp.register_callback_query_handler(confirm_delete_review)
