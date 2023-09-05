__all__ = ['register_users_student_schedule']


from .student_schedule import student_schedule
from .enter_student import enter_student
from .pick_student_menu import pick_student_menu
from .tomorrow_student_schedule import tomorrow_student_schedule
from .calendar_student_schedule import calendar_student_schedule
from .process_calendar_student_schedule import process_calendar_student_schedule
from .weekly_student_schedule import weekly_student_schedule

from aiogram import Dispatcher


def register_users_student_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(student_schedule)
    dp.register_message_handler(enter_student)
    dp.register_callback_query_handler(pick_student_menu)
    dp.register_callback_query_handler(tomorrow_student_schedule)
    dp.register_callback_query_handler(calendar_student_schedule)
    dp.register_callback_query_handler(process_calendar_student_schedule)
    dp.register_callback_query_handler(weekly_student_schedule)
