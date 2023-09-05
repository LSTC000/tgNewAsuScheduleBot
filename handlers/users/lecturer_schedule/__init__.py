__all__ = ['register_users_lecturer_schedule']


from .lecturer_schedule import lecturer_schedule
from .enter_lecturer import enter_lecturer
from .pick_lecturer_menu import pick_lecturer_menu
from .tomorrow_lecturer_schedule import tomorrow_lecturer_schedule
from .calendar_lecturer_schedule import calendar_lecturer_schedule
from .process_calendar_lecturer_schedule import process_calendar_lecturer_schedule
from .weekly_lecturer_schedule import weekly_lecturer_schedule

from aiogram import Dispatcher


def register_users_lecturer_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(lecturer_schedule)
    dp.register_message_handler(enter_lecturer)
    dp.register_callback_query_handler(pick_lecturer_menu)
    dp.register_callback_query_handler(tomorrow_lecturer_schedule)
    dp.register_callback_query_handler(calendar_lecturer_schedule)
    dp.register_callback_query_handler(process_calendar_lecturer_schedule)
    dp.register_callback_query_handler(weekly_lecturer_schedule)
