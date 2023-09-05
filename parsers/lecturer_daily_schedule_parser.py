from urllib.parse import quote

from data.config import JSON_TOKEN

from data.redis import LECTURER_NAME_REDIS_KEY, LECTURER_URL_REDIS_KEY

from data.urls import JSON_LECTURERS_SCHEDULE_QUERY_URL

from functions import get_lecturers_data, get_lecturer_data

from utils import create_lecturer_daily_schedule_report

from aiogram.dispatcher.storage import FSMContext


async def lecturer_daily_schedule_parser(
    user_id: int,
    date_code: str,
    state: FSMContext,
    today: bool = True,
    calendar: bool = False,
) -> tuple:
    """
    :param user_id: Telegram user id.
    :param date_code: Date code for url query.
    :param state: FSMContext.
    :param today: True - if we want to get a today lecturer schedule. False - if we want to get a tomorrow lecturer
    schedule. Default: True.
    :param calendar: True - if we want to get a calendar lecturer schedule, else - False.
    :return:
        Tuple:
            students_data - Dictionary with all matching lecturers found.
            schedule_report - A line with a schedule for the lecturer on the selected day, if there is no schedule,
            then an empty line.
    """
    lecturers_data, schedule_report, lecturer_url = {}, '', ''

    async with state.proxy() as data:
        if LECTURER_URL_REDIS_KEY in data:
            lecturer_url = data[LECTURER_URL_REDIS_KEY]

        lecturer_name = data[LECTURER_NAME_REDIS_KEY]

    if not lecturer_url:
        lecturer_name_encoded = quote(lecturer_name, safe='+:/?=&')
        lecturers_url = JSON_LECTURERS_SCHEDULE_QUERY_URL.format(lecturer_name_encoded, JSON_TOKEN)

        over_max_length, lecturers_data = await get_lecturers_data(user_id=user_id, lecturers_url=lecturers_url)

        if over_max_length:
            return True, schedule_report

        if not lecturers_data:
            return lecturers_data, schedule_report

        if len(lecturers_data.keys()) > 1:
            return lecturers_data, True

        for lecturer_id in lecturers_data.keys():
            lecturer_name = lecturers_data[lecturer_id]['name']
            lecturer_url = lecturers_data[lecturer_id]['url']

        lecturers_data = {}

        async with state.proxy() as data:
            data[LECTURER_NAME_REDIS_KEY] = lecturer_name
            data[LECTURER_URL_REDIS_KEY] = lecturer_url

    no_classes, lecturer_data = await get_lecturer_data(
        user_id=user_id,
        lecturer_url=lecturer_url,
        date_code=date_code
    )

    if no_classes or lecturer_data:
        return lecturers_data, create_lecturer_daily_schedule_report(
            lecturer_name=lecturer_name,
            lecturer_url=lecturer_url,
            lecturer_data=lecturer_data,
            no_classes=no_classes,
            today=today,
            date_code=date_code if calendar else ''
        )
    else:
        return lecturer_data, schedule_report
