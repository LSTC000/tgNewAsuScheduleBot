__all__ = ['register_admins_alert_for_users']


from .alert_for_users import alert_for_users
from .enter_alert_for_users import enter_alert_for_users
from .confirm_alert_for_users import confirm_alert_for_users

from aiogram import Dispatcher


def register_admins_alert_for_users(dp: Dispatcher):
    dp.register_callback_query_handler(alert_for_users)
    dp.register_message_handler(enter_alert_for_users)
    dp.register_callback_query_handler(confirm_alert_for_users)
