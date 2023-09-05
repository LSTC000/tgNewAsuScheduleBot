__all__ = ['register_users_main_menu']


from .change_user_alert import change_user_alert
from .asu_buildings import asu_buildings
from .help import help
from .last_student_schedule import last_student_schedule
from .last_lecturer_schedule import last_lecturer_schedule

from aiogram import Dispatcher


def register_users_main_menu(dp: Dispatcher):
    dp.register_callback_query_handler(change_user_alert)
    dp.register_callback_query_handler(asu_buildings)
    dp.register_callback_query_handler(help)
    dp.register_callback_query_handler(last_student_schedule)
    dp.register_callback_query_handler(last_lecturer_schedule)
