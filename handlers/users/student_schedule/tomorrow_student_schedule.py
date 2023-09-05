from loader import dp, bot, schedule_cache

from data.callbacks import TOMORROW_SCHEDULE_CALLBACK_DATA

from data.redis import TOMORROW_DATE_CODE_REDIS_KEY, STUDENT_NAME_REDIS_KEY

from parsers import student_daily_schedule_parser

from functions import clear_last_ikb, call_schedule_menu_ikb, process_student_daily_schedule_parser

from states import StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == TOMORROW_SCHEDULE_CALLBACK_DATA,
    state=StudentScheduleStatesGroup.schedule_menu
)
async def tomorrow_student_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        student_name = data[STUDENT_NAME_REDIS_KEY]
        tomorrow_date_code = data[TOMORROW_DATE_CODE_REDIS_KEY]

    key_cache = f'{student_name}_{tomorrow_date_code}'
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
            date_code=tomorrow_date_code,
            state=state,
            today=False
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
