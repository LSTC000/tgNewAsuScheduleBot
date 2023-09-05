__all__ = ['register_users_socials']


from .social_menu import social_menu

from aiogram import Dispatcher


def register_users_socials(dp: Dispatcher):
    dp.register_callback_query_handler(social_menu)
