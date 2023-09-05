from data.redis import LECTURER_NAME_REDIS_KEY, LECTURER_URL_REDIS_KEY

from functions import get_weekly_lecturer_data

from utils import create_lecturer_weekly_schedule_report

from aiogram.dispatcher.storage import FSMContext


async def lecturer_weekly_schedule_parser(
    user_id: int,
    state: FSMContext
) -> tuple:
    """
    :param user_id: Telegram user id.
    :param state: FSMContext.
    :return:
        Tuple:
            weekly_lecturer_data - True - if weekly_lecturer_data is not empty, else - False.
            weekly_schedule_report - A line with a schedule for the lecturer on week, if there is no schedule,
            then an empty line.
    """
    weekly_schedule_report = ''

    async with state.proxy() as data:
        lecturer_url = data[LECTURER_URL_REDIS_KEY]
        lecturer_name = data[LECTURER_NAME_REDIS_KEY]

    no_classes, weekly_lecturer_data = await get_weekly_lecturer_data(
        user_id=user_id,
        lecturer_url=lecturer_url
    )

    if no_classes or weekly_lecturer_data:
        return True, create_lecturer_weekly_schedule_report(
            lecturer_name=lecturer_name,
            lecturer_url=lecturer_url,
            weekly_lecturer_data=weekly_lecturer_data,
            no_classes=no_classes
        )
    else:
        return False, weekly_schedule_report
