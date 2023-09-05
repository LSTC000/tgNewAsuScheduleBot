import json
from datetime import datetime

from data.config import REQUEST_HEADERS, JSON_TOKEN

from data.urls import JSON_DATE_QUERY_URL, FREE_ROOMS_URL_DICT

import httpx


async def get_lecturer_data(
    user_id: int,
    lecturer_url: str,
    date_code: str
) -> tuple:
    """
    :param user_id: Telegram user id.
    :param lecturer_url: Url to the weekly lecturer schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param date_code: Date code for url query.
        Example: '20230326'.
    :return:
        Bool: True - lecturer don`t has a classes today, else - False.
        Dict - Contains the key - the name of the table header and the value - the header data.
    """

    no_classes, lecturer_data = False, {}

    # Create an url to find the daily schedule.
    date_query_url = JSON_DATE_QUERY_URL.format(lecturer_url, date_code, JSON_TOKEN)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=date_query_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return no_classes, lecturer_data

    try:
        data = response.json()
        schedule_data = data.get('schedule')

        rows = schedule_data.get('rows')

        # Checking whether there are classes or not.
        if not rows:
            return True, lecturer_data

        records = schedule_data.get('records')

        lecturer_data = {
            'date': datetime.strptime(date_code, "%Y%m%d").strftime("%a %d-%m-%Y"),
            'order': [],
            'time': [],
            'subject': [],
            'group': [],
            'room': [],
            'free_rooms': []
        }

        for record in records:
            # Add lesson order.
            try:
                lecturer_data['order'].append(record.get('lessonNum'))
            except KeyError:
                lecturer_data['order'].append('')
            # Add lesson time.
            try:
                lecturer_data['time'].append(f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
            except KeyError:
                lecturer_data['time'].append('')
            # Add lesson subject.
            try:
                subject = record.get('lessonSubject')
                try:
                    subject_type = record.get('lessonSubjectType')
                    lecturer_data['subject'].append(subject_type + ' ' + subject.get('subjectTitle'))
                except KeyError:
                    lecturer_data['subject'].append(subject.get('subjectTitle'))
            except KeyError:
                lecturer_data['subject'].append('')
            # Add lesson groups.
            try:
                groups = record.get('lessonGroups')
                groups_list = []

                for group in groups:
                    groups_list.append(group.get('lessonGroup').get('groupCode') + ' ' + group.get('lessonSubGroup'))

                lecturer_data['group'].append(', '.join(groups_list))
            except KeyError:
                lecturer_data['group'].append('')
            # Add lesson room.
            try:
                room = record.get('lessonRoom')
                lecturer_data['room'].append(f"{room.get('roomTitle')} {room.get('roomBuildingCode')}")
            except KeyError:
                lecturer_data['room'].append('')
            # Add url to free rooms.
            try:
                room = record.get('lessonRoom')
                building_code = room.get('roomBuildingCode').lower()
                if building_code in FREE_ROOMS_URL_DICT:
                    lesson_time = record.get('lessonTimeStart').replace(':', '') + record.get('lessonTimeEnd').replace(
                        ':', '')
                    lesson_num = int(record.get('lessonNum'))
                    lesson_num = f'0{lesson_num}' if lesson_num < 10 else f'{lesson_num}'
                    lecturer_data['free_rooms'].append(
                        FREE_ROOMS_URL_DICT[building_code].format(date_code + lesson_time + lesson_num)
                    )
                else:
                    lecturer_data['free_rooms'].append('')
            except KeyError:
                lecturer_data['free_rooms'].append('')

        return no_classes, lecturer_data
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return no_classes, lecturer_data
