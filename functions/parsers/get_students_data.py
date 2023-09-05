import json

from data.config import REQUEST_HEADERS, MAX_INLINE_KEYBOARD_LENGTH

from data.urls import STUDENT_SCHEDULE_URL

import httpx


async def get_students_data(user_id: int, students_url: str) -> tuple:
    """
    :param user_id: Telegram user id.
    :param students_url: Url to search for the alleged students.
        Example: https://www.asu.ru/timetable/search/students/?query=404.
    :return:
        Tuple:
            Bool: True - if count of alleged students over MAX_INLINE_KEYBOARD_LENGTH.
            Dict: The key - group number, the value is a list of the group name and a link to it.
            If an error occurs, then an empty dictionary.
    """

    over_max_length, students_data = False, {}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=students_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return over_max_length, students_data

    try:
        data = response.json()
        groups = data.get('groups')
        rows = groups.get('rows')

        # Checking for the number of matches found with the name of the alleged student.
        if not rows:
            return over_max_length, students_data
        # Checking for an acceptable threshold for the number of possible alleged students.
        if rows > MAX_INLINE_KEYBOARD_LENGTH:
            return True, students_data

        records = groups.get('records')

        for i, record in enumerate(records):
            students_data[i] = {
                'name': record.get('groupCode'),
                'url': STUDENT_SCHEDULE_URL.format(record.get('path'))
            }

        return over_max_length, students_data
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return over_max_length, students_data
