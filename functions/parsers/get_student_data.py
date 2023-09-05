import json
from datetime import datetime

from data.config import REQUEST_HEADERS, JSON_TOKEN

from data.urls import JSON_DATE_QUERY_URL, FREE_ROOMS_URL_DICT

import httpx


async def get_student_data(
    user_id: int,
    student_url: str,
    date_code: str
) -> tuple:
    """
    :param user_id: Telegram user id.
    :param student_url: Url to the weekly student schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param date_code: Date code for url query.
        Example: '20230326'.
    :return:
        Bool: True - student don`t has a classes today, else - False.
        Dict - Contains the key - the name of the table header and the value - the header data.
    """

    no_classes, student_data = False, {}

    # Create an url to find the daily schedule.
    date_query_url = JSON_DATE_QUERY_URL.format(student_url, date_code, JSON_TOKEN)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=date_query_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return no_classes, student_data

    try:
        data = response.json()
        schedule_data = data.get('schedule')

        rows = schedule_data.get('rows')

        # Checking whether there are classes or not.
        if not rows:
            return True, student_data

        records = schedule_data.get('records')

        student_data = {
            'date': datetime.strptime(date_code, "%Y%m%d").strftime("%a %d-%m-%Y"),
            'order': [],
            'time': [],
            'subject': [],
            'lecturer': [],
            'room': [],
            'free_rooms': []
        }

        for record in records:
            # Add lesson order.
            try:
                student_data['order'].append(record.get('lessonNum'))
            except KeyError:
                student_data['order'].append('')
            # Add lesson time.
            try:
                student_data['time'].append(f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
            except KeyError:
                student_data['time'].append('')
            # Add lesson subject.
            try:
                subject = record.get('lessonSubject')
                try:
                    lesson_group = record.get('lessonGroups')[0].get('lessonSubGroup')
                    subject_type = record.get('lessonSubjectType')
                    if lesson_group:
                        student_data['subject'].append(lesson_group + ' ' + subject_type + ' ' + subject.get('subjectTitle'))
                    else:
                        student_data['subject'].append(subject_type + ' ' + subject.get('subjectTitle'))
                except (KeyError, IndexError):
                    student_data['subject'].append(subject.get('subjectTitle'))
            except KeyError:
                student_data['subject'].append('')
            # Add lesson lecturers.
            try:
                lecturers = record.get('lessonLecturers')
                lecturers_list = []

                for lecturer in lecturers:
                    lecturers_list.append(f"{lecturer.get('lecturerName')} ({lecturer.get('lecturerPosition')})")

                student_data['lecturer'].append(', '.join(lecturers_list))
            except KeyError:
                student_data['lecturer'].append('')
            # Add lesson room.
            try:
                room = record.get('lessonRoom')
                student_data['room'].append(f"{room.get('roomTitle')} {room.get('roomBuildingCode')}")
            except KeyError:
                student_data['room'].append('')
            # Add url to free rooms.
            try:
                room = record.get('lessonRoom')
                building_code = room.get('roomBuildingCode').lower()
                if building_code in FREE_ROOMS_URL_DICT:
                    lesson_time = (record.get('lessonTimeStart').replace(':', '') +
                                   record.get('lessonTimeEnd').replace(':', ''))
                    lesson_num = int(record.get('lessonNum'))
                    lesson_num = f'0{lesson_num}' if lesson_num < 10 else f'{lesson_num}'
                    student_data['free_rooms'].append(
                        FREE_ROOMS_URL_DICT[building_code].format(date_code + lesson_time + lesson_num)
                    )
                else:
                    student_data['free_rooms'].append('')
            except KeyError:
                student_data['free_rooms'].append('')

        return no_classes, student_data
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return no_classes, student_data
