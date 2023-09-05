from data.redis import STUDENT_NAME_REDIS_KEY, STUDENT_URL_REDIS_KEY

from functions import get_weekly_student_data

from utils import create_student_weekly_schedule_report

from aiogram.dispatcher.storage import FSMContext


async def student_weekly_schedule_parser(
    user_id: int,
    state: FSMContext
) -> tuple:
    """
    :param user_id: Telegram user id.
    :param state: FSMContext.
    :return:
        Tuple:
            weekly_student_data - True - if weekly_student_data is not empty, else - False.
            weekly_schedule_report - A line with a schedule for the student on week, if there is no schedule,
            then an empty line.
    """
    weekly_schedule_report = ''

    async with state.proxy() as data:
        student_url = data[STUDENT_URL_REDIS_KEY]
        student_name = data[STUDENT_NAME_REDIS_KEY]

    no_classes, weekly_student_data = await get_weekly_student_data(
        user_id=user_id,
        student_url=student_url
    )

    if no_classes or weekly_student_data:
        return True, create_student_weekly_schedule_report(
            student_name=student_name,
            student_url=student_url,
            weekly_student_data=weekly_student_data,
            no_classes=no_classes
        )
    else:
        return False, weekly_schedule_report
