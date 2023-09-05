from loader import dp, bot, schedule_cache

from data.callbacks import CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA

from data.redis import STUDENT_NAME_REDIS_KEY

from parsers import student_daily_schedule_parser

from functions import clear_last_ikb, call_schedule_menu_ikb, process_student_daily_schedule_parser

from pickers import Calendar

from states import StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data != CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA,
    state=StudentScheduleStatesGroup.calendar_picker
)
async def process_calendar_student_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    callback_data = callback.data

    pick, date_code = await Calendar().process_selection(
        callback=callback,
        callback_data=callback_data,
        state=state
    )

    if pick:
        async with state.proxy() as data:
            student_name = data[STUDENT_NAME_REDIS_KEY]

        key_cache = f'{student_name}_{date_code}'
        if key_cache in schedule_cache:
            # Clear last inline keyboard.
            await clear_last_ikb(user_id=user_id, state=state)

            await bot.send_message(chat_id=user_id, text=schedule_cache[key_cache]['report'])

            # Call schedule inline menu.
            await call_schedule_menu_ikb(user_id=user_id, state=state)
            # Set schedule_menu state.
            await StudentScheduleStatesGroup.schedule_menu.set()
        else:
            students_data, schedule_report = await student_daily_schedule_parser(
                user_id=user_id,
                date_code=date_code,
                state=state,
                today=False,
                calendar=True
            )

            await process_student_daily_schedule_parser(
                user_id=user_id,
                students_data=students_data,
                schedule_report=schedule_report,
                key_cache=key_cache,
                state=state,
                update=False,
                clear=True
            )
