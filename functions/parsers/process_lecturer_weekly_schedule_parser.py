from loader import bot, schedule_cache

from data.messages import ERROR_LECTURER_WEEKLY_SCHEDULE_MESSAGE

from data.urls import SCHEDULE_ASU_URL

from functions import clear_last_ikb, call_schedule_menu_ikb

from aiogram.dispatcher.storage import FSMContext


async def process_lecturer_weekly_schedule_parser(
    user_id: int,
    weekly_lecturer_data: bool,
    weekly_schedule_report: list,
    key_cache: str,
    state: FSMContext
) -> None:
    """
    :param user_id: Telegram user id.
    :param weekly_lecturer_data: True - if weekly_lecturer_data is not empty, else - False.
    :param weekly_schedule_report: List with lecturer daily schedule report.
    :param key_cache: Key of schedule_cache.
    :param state: FSMContext.
    """

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if weekly_lecturer_data:
        schedule_cache[key_cache] = {'weekly_report': weekly_schedule_report}

        for schedule_report in weekly_schedule_report:
            await bot.send_message(chat_id=user_id, text=schedule_report)
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_LECTURER_WEEKLY_SCHEDULE_MESSAGE.format(SCHEDULE_ASU_URL))

    # Call schedule inline menu.
    await call_schedule_menu_ikb(user_id=user_id, state=state)
