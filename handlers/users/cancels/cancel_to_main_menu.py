from loader import dp

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from functions import clear_last_ikb, clear_redis_data, call_main_menu_ikb

from states import (
    MainMenuStatesGroup,
    SocialStatesGroup,
    AdminMenuStatesGroup,
    StudentScheduleStatesGroup,
    LecturerScheduleStatesGroup,
)

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_MAIN_MENU_CALLBACK_DATA,
    state=[
        MainMenuStatesGroup.asu_buildings,
        MainMenuStatesGroup.help,
        SocialStatesGroup.social_menu,
        AdminMenuStatesGroup.admin_menu,
        StudentScheduleStatesGroup.schedule_menu,
        StudentScheduleStatesGroup.pick_student_menu,
        LecturerScheduleStatesGroup.pick_lecturer_menu,
        LecturerScheduleStatesGroup.schedule_menu,
    ]
)
async def cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear redis data.
    await clear_redis_data(state=state)
    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call main inline menu.
    await call_main_menu_ikb(user_id=user_id, state=state)
    # Set main_menu state.
    await MainMenuStatesGroup.main_menu.set()
