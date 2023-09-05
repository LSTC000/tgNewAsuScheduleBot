from loader import dp, bot, schedule_cache

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.redis import TODAY_DATE_CODE_REDIS_KEY, STUDENTS_DATA_REDIS_KEY, STUDENT_NAME_REDIS_KEY, STUDENT_URL_REDIS_KEY

from parsers import student_daily_schedule_parser

from functions import (
    clear_last_ikb,
    call_schedule_menu_ikb,
    process_student_daily_schedule_parser,
    UserInfoCache
)


from states import StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data != CANCEL_TO_MAIN_MENU_CALLBACK_DATA,
    state=StudentScheduleStatesGroup.pick_student_menu
)
async def pick_student_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    callback_data = callback.data

    async with state.proxy() as data:
        today_date_code = data[TODAY_DATE_CODE_REDIS_KEY]
        student_name = data[STUDENTS_DATA_REDIS_KEY][callback_data]['name']

        data[STUDENT_NAME_REDIS_KEY] = student_name
        data[STUDENT_URL_REDIS_KEY] = data[STUDENTS_DATA_REDIS_KEY][callback_data]['url']

        data.pop(STUDENTS_DATA_REDIS_KEY)
        data.pop(TODAY_DATE_CODE_REDIS_KEY)

    key_cache = f'{student_name}_{today_date_code}'
    if key_cache in schedule_cache:
        # Update student data in the database.
        await UserInfoCache(user_id).update_student_data_cache(
            student_name=schedule_cache[key_cache]['name'],
            student_url=schedule_cache[key_cache]['url']
        )

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
            date_code=today_date_code,
            state=state
        )

        await process_student_daily_schedule_parser(
            user_id=user_id,
            students_data=students_data,
            schedule_report=schedule_report,
            key_cache=key_cache,
            state=state,
            clear=True
        )
