from loader import dp

from data.callbacks import CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA

from functions import clear_last_ikb, call_schedule_menu_ikb

from states import StudentScheduleStatesGroup, LecturerScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA,
    state=[
        StudentScheduleStatesGroup.calendar_picker,
        LecturerScheduleStatesGroup.calendar_picker
    ]
)
async def cancel_to_schedule_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Call schedule inline menu.
    await call_schedule_menu_ikb(user_id=user_id, state=state)

    if await state.get_state() == StudentScheduleStatesGroup.calendar_picker.state:
        # Set schedule_menu state.
        await StudentScheduleStatesGroup.schedule_menu.set()
    else:
        # Set schedule_menu state.
        await LecturerScheduleStatesGroup.schedule_menu.set()
