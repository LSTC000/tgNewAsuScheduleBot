from loader import bot, schedule_cache

from data.messages import ERROR_STUDENT_WEEKLY_SCHEDULE_MESSAGE

from data.urls import SCHEDULE_ASU_URL

from functions import clear_last_ikb, call_schedule_menu_ikb

from aiogram.dispatcher.storage import FSMContext


async def process_student_weekly_schedule_parser(
    user_id: int,
    weekly_student_data: bool,
    weekly_schedule_report: list,
    key_cache: str,
    state: FSMContext
) -> None:
    """
    :param user_id: Telegram user id.
    :param weekly_student_data: True - if weekly_student_data is not empty, else - False.
    :param weekly_schedule_report: List with student daily schedule report.
    :param key_cache: Key of schedule_cache.
    :param state: FSMContext.
    """

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    if weekly_student_data:
        schedule_cache[key_cache] = {'weekly_report': weekly_schedule_report}

        for schedule_report in weekly_schedule_report:
            await bot.send_message(chat_id=user_id, text=schedule_report)
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_STUDENT_WEEKLY_SCHEDULE_MESSAGE.format(SCHEDULE_ASU_URL))

    # Call schedule inline menu.
    await call_schedule_menu_ikb(user_id=user_id, state=state)
