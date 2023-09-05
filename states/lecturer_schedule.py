from aiogram.dispatcher.filters.state import StatesGroup, State


class LecturerScheduleStatesGroup(StatesGroup):
    enter_lecturer = State()
    pick_lecturer_menu = State()
    schedule_menu = State()
    calendar_picker = State()
