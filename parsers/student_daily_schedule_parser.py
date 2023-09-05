from urllib.parse import quote

from data.config import JSON_TOKEN

from data.redis import STUDENT_NAME_REDIS_KEY, STUDENT_URL_REDIS_KEY

from data.urls import JSON_STUDENTS_SCHEDULE_QUERY_URL

from functions import get_students_data, get_student_data

from utils import create_student_daily_schedule_report

from aiogram.dispatcher.storage import FSMContext


async def student_daily_schedule_parser(
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
    :param today: True - if we want to get a today student schedule. False - if we want to get a tomorrow student
    schedule. Default: True.
    :param calendar: True - if we want to get a calendar student schedule, else - False.
    :return:
        Tuple:
            students_data - Dictionary with all matching groups found.
            schedule_report - A line with a schedule for the student on the selected day, if there is no schedule,
            then an empty line.
    """
    students_data, schedule_report, student_url = {}, '', ''

    async with state.proxy() as data:
        if STUDENT_URL_REDIS_KEY in data:
            student_url = data[STUDENT_URL_REDIS_KEY]

        student_name = data[STUDENT_NAME_REDIS_KEY]

    if not student_url:
        student_name_encoded = quote(student_name, safe='+:/?=&')
        students_url = JSON_STUDENTS_SCHEDULE_QUERY_URL.format(student_name_encoded, JSON_TOKEN)

        over_max_length, students_data = await get_students_data(user_id=user_id, students_url=students_url)

        if over_max_length:
            return True, schedule_report

        if not students_data:
            return students_data, schedule_report

        if len(students_data.keys()) > 1:
            return students_data, True

        for student_id in students_data.keys():
            student_name = students_data[student_id]['name']
            student_url = students_data[student_id]['url']

        students_data = {}

        async with state.proxy() as data:
            data[STUDENT_NAME_REDIS_KEY] = student_name
            data[STUDENT_URL_REDIS_KEY] = student_url

    no_classes, student_data = await get_student_data(
        user_id=user_id,
        student_url=student_url,
        date_code=date_code
    )

    if no_classes or student_data:
        return students_data, create_student_daily_schedule_report(
            student_name=student_name,
            student_url=student_url,
            student_data=student_data,
            no_classes=no_classes,
            today=today,
            date_code=date_code if calendar else ''
        )
    else:
        return student_data, schedule_report
