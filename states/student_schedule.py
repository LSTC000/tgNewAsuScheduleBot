from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentScheduleStatesGroup(StatesGroup):
    enter_student = State()
    pick_student_menu = State()
    schedule_menu = State()
    calendar_picker = State()
