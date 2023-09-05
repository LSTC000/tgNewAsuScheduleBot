from datetime import datetime

from data.config import DAY_CONVERT_DICT, ORDER_CONVERT_DICT, CONVERT_TABLE_HEADERS

from data.messages import (
    NO_CLASSES_TODAY_STUDENT_MESSAGE,
    NO_CLASSES_TOMORROW_STUDENT_MESSAGE,
    NO_CLASSES_CALENDAR_STUDENT_MESSAGE
)

from .find_building_location import find_building_location


def create_student_daily_schedule_report(
    student_name: str,
    student_url: str,
    student_data: dict,
    no_classes: bool,
    today: bool,
    date_code: str
) -> str:
    """
    :param student_name: Student name.
    :param student_url: Url to the weekly student schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param student_data: Contains the key - the name of the table header and the value - the header data.
    :param no_classes: True - student don`t has a classes today, else - False.
    :param today: True - if we want to get a today student schedule. False - if we want to get a tomorrow student
    schedule.
    :param date_code: Date code for url query.
    :return: Student schedule report.
    """

    if no_classes:
        if date_code:
            schedule_report = NO_CLASSES_CALENDAR_STUDENT_MESSAGE.format(
                datetime.strptime(date_code, '%Y%m%d').strftime('%d-%m-%Y'), student_url
            )
        elif today:
            schedule_report = NO_CLASSES_TODAY_STUDENT_MESSAGE.format(student_url)
        else:
            schedule_report = NO_CLASSES_TOMORROW_STUDENT_MESSAGE.format(student_url)
    else:
        date = student_data['date'].split()

        schedule_report = f'👨‍🎓 <b>{student_name}</b>\n\n' \
            f'📌 <u><b>{DAY_CONVERT_DICT[date[0]]}</b> {date[-1]}</u>\n\n'

        for i in range(len(student_data['order'])):
            for header in ['order', 'time', 'subject', 'lecturer', 'room', 'free_rooms']:
                if header == 'order':
                    schedule_report += f'{ORDER_CONVERT_DICT[student_data[header][i]]}\n'
                elif header == 'room':
                    schedule_report += (f'{CONVERT_TABLE_HEADERS[header]} '
                                        f'{find_building_location(student_data[header][i])}\n')
                elif header == 'free_rooms':
                    if student_data[header][i]:
                        schedule_report += f'<a href="{student_data[header][i]}" title="свободные аудитории">' \
                                  f'<b>{CONVERT_TABLE_HEADERS[header]}</b></a>\n'
                else:
                    schedule_report += f'{CONVERT_TABLE_HEADERS[header]} {student_data[header][i]}\n'

            schedule_report += '\n'

        schedule_report += f'🚀 <a href="{student_url}" title="расписание"><b>Расписание на текущую неделю</b></a>'

    return schedule_report
