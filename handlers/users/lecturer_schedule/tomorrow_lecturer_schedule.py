from loader import dp, bot, schedule_cache

from data.callbacks import TOMORROW_SCHEDULE_CALLBACK_DATA

from data.redis import TOMORROW_DATE_CODE_REDIS_KEY, LECTURER_NAME_REDIS_KEY

from parsers import lecturer_daily_schedule_parser

from functions import clear_last_ikb, call_schedule_menu_ikb, process_lecturer_daily_schedule_parser

from states import LecturerScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == TOMORROW_SCHEDULE_CALLBACK_DATA,
    state=LecturerScheduleStatesGroup.schedule_menu
)
async def tomorrow_lecturer_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        lecturer_name = data[LECTURER_NAME_REDIS_KEY]
        tomorrow_date_code = data[TOMORROW_DATE_CODE_REDIS_KEY]

    key_cache = f'{lecturer_name}_{tomorrow_date_code}'
    if key_cache in schedule_cache:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)

        await bot.send_message(chat_id=user_id, text=schedule_cache[key_cache]['report'])

        # Call schedule inline menu.
        await call_schedule_menu_ikb(user_id=user_id, state=state)
        # Set schedule_menu state.
        await LecturerScheduleStatesGroup.schedule_menu.set()
    else:
        lecturers_data, schedule_report = await lecturer_daily_schedule_parser(
            user_id=user_id,
            date_code=tomorrow_date_code,
            state=state,
            today=False
        )

        await process_lecturer_daily_schedule_parser(
            user_id=user_id,
            lecturers_data=lecturers_data,
            schedule_report=schedule_report,
            key_cache=key_cache,
            state=state,
            update=False,
            clear=True
        )
