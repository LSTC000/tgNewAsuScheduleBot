from loader import dp, bot, schedule_cache

from data.callbacks import WEEKLY_SCHEDULE_CALLBACK_DATA

from data.redis import STUDENT_NAME_REDIS_KEY

from parsers import student_weekly_schedule_parser

from functions import clear_last_ikb, call_schedule_menu_ikb, process_student_weekly_schedule_parser

from states import StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == WEEKLY_SCHEDULE_CALLBACK_DATA,
    state=StudentScheduleStatesGroup.schedule_menu
)
async def weekly_student_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        student_name = data[STUDENT_NAME_REDIS_KEY]

    key_cache = f'{student_name}_weekly'
    if key_cache in schedule_cache:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)

        for schedule_report in schedule_cache[key_cache]['weekly_report']:
            await bot.send_message(chat_id=user_id, text=schedule_report)

        # Call schedule inline menu.
        await call_schedule_menu_ikb(user_id=user_id, state=state)
    else:
        weekly_student_data, weekly_schedule_report = await student_weekly_schedule_parser(
            user_id=user_id,
            state=state,
        )

        await process_student_weekly_schedule_parser(
            user_id=user_id,
            weekly_student_data=weekly_student_data,
            weekly_schedule_report=weekly_schedule_report,
            key_cache=key_cache,
            state=state
        )
