import json

from data.config import REQUEST_HEADERS, MAX_INLINE_KEYBOARD_LENGTH

from data.urls import LECTURER_SCHEDULE_URL

import httpx


async def get_lecturers_data(user_id: int, lecturers_url: str) -> tuple:
    """
    :param user_id: Telegram user id.
    :param lecturers_url: Url to search for the alleged lecturers.
        Example: https://www.asu.ru/timetable/search/students/?query=404.
    :return:
        Tuple:
            Bool: True - if count of alleged lecturers over MAX_INLINE_KEYBOARD_LENGTH.
            Dict: The key - lecturer number, the value is a list of the lecturer name and a link to it.
            If an error occurs, then an empty dictionary.
    """

    over_max_length, lecturers_data = False, {}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=lecturers_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return over_max_length, lecturers_data

    try:
        data = response.json()
        lecturers = data.get('lecturers')
        rows = lecturers.get('rows')

        # Checking for the number of matches found with the name of the alleged lecturer.
        if not rows:
            return over_max_length, lecturers_data
        # Checking for an acceptable threshold for the number of possible alleged lecturers.
        if rows > MAX_INLINE_KEYBOARD_LENGTH:
            return True, lecturers_data

        records = lecturers.get('records')

        for i, record in enumerate(records):
            try:
                name = f"{record.get('lecturerName')} ({record.get('lecturerPosition')})"
            except KeyError:
                name = f"{record.get('lecturerName')}"

            lecturers_data[i] = {
                'name': name,
                'url': LECTURER_SCHEDULE_URL.format(record.get('path'))
            }

        return over_max_length, lecturers_data
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return over_max_length, lecturers_data
