from loader import dp, bot, schedule_cache

from data.callbacks import WEEKLY_SCHEDULE_CALLBACK_DATA

from data.redis import LECTURER_NAME_REDIS_KEY

from parsers import lecturer_weekly_schedule_parser

from functions import clear_last_ikb, call_schedule_menu_ikb, process_lecturer_weekly_schedule_parser

from states import LecturerScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == WEEKLY_SCHEDULE_CALLBACK_DATA,
    state=LecturerScheduleStatesGroup.schedule_menu
)
async def weekly_lecturer_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        lecturer_name = data[LECTURER_NAME_REDIS_KEY]

    key_cache = f'{lecturer_name}_weekly'
    if key_cache in schedule_cache:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)

        for schedule_report in schedule_cache[key_cache]['weekly_report']:
            await bot.send_message(chat_id=user_id, text=schedule_report)

        # Call schedule inline menu.
        await call_schedule_menu_ikb(user_id=user_id, state=state)
    else:
        weekly_lecturer_data, weekly_schedule_report = await lecturer_weekly_schedule_parser(
            user_id=user_id,
            state=state,
        )

        await process_lecturer_weekly_schedule_parser(
            user_id=user_id,
            weekly_lecturer_data=weekly_lecturer_data,
            weekly_schedule_report=weekly_schedule_report,
            key_cache=key_cache,
            state=state
        )
