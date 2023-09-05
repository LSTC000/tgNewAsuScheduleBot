from loader import dp, bot, schedule_stt, schedule_cache

from data.messages import VOICE_TO_TEXT_CONVERT_ERROR_MESSAGE

from data.redis import TODAY_DATE_CODE_REDIS_KEY, TOMORROW_DATE_CODE_REDIS_KEY, STUDENT_NAME_REDIS_KEY

from parsers import student_daily_schedule_parser

from functions import (
    call_main_menu_ikb,
    call_schedule_menu_ikb,
    voice_to_text_convert,
    process_student_daily_schedule_parser,
    UserInfoCache
)

from ner import text_to_student_convert

from states import MainMenuStatesGroup, StudentScheduleStatesGroup

from utils import get_date_codes

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(
    content_types=[types.ContentType.TEXT, types.ContentType.VOICE],
    state=StudentScheduleStatesGroup.enter_student
)
async def enter_student(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if message.content_type == 'voice':
        student_name = await voice_to_text_convert(
            user_id=user_id,
            file_id=message.voice.file_id,
            stt=schedule_stt
        )
        if student_name is not None:
            student_name = await text_to_student_convert(text=student_name)
    else:
        student_name = message.text

    if student_name is None:
        await bot.send_message(chat_id=user_id, text=VOICE_TO_TEXT_CONVERT_ERROR_MESSAGE)
        # Call main inline menu.
        await call_main_menu_ikb(user_id=user_id, state=state)
        # Set main_menu state.
        await MainMenuStatesGroup.main_menu.set()
    else:
        today_date_code, tomorrow_date_code = get_date_codes()

        async with state.proxy() as data:
            data[STUDENT_NAME_REDIS_KEY] = student_name
            data[TODAY_DATE_CODE_REDIS_KEY] = today_date_code
            data[TOMORROW_DATE_CODE_REDIS_KEY] = tomorrow_date_code

        key_cache = f'{student_name}_{today_date_code}'
        if key_cache in schedule_cache:
            # Update student data in the database.
            await UserInfoCache(user_id).update_student_data_cache(
                student_name=schedule_cache[key_cache]['name'],
                student_url=schedule_cache[key_cache]['url']
            )

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
                state=state
            )
