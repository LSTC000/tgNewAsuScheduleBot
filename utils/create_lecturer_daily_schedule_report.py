from datetime import datetime

from data.config import DAY_CONVERT_DICT, ORDER_CONVERT_DICT, CONVERT_TABLE_HEADERS

from data.messages import (
    NO_CLASSES_TODAY_LECTURER_MESSAGE,
    NO_CLASSES_TOMORROW_LECTURER_MESSAGE,
    NO_CLASSES_CALENDAR_LECTURER_MESSAGE
)

from .find_building_location import find_building_location


def create_lecturer_daily_schedule_report(
    lecturer_name: str,
    lecturer_url: str,
    lecturer_data: dict,
    no_classes: bool,
    today: bool,
    date_code: str
) -> str:
    """
    :param lecturer_name: Lecturer name.
    :param lecturer_url: Url to the weekly lecturer schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param lecturer_data: Contains the key - the name of the table header and the value - the header data.
    :param no_classes: True - lecturer don`t has a classes today, else - False.
    :param today: True - if we want to get a today lecturer schedule. False - if we want to get a tomorrow lecturer
    schedule.
    :param date_code: Date code for url query.
    :return: Lecturer schedule report.
    """

    if no_classes:
        if date_code:
            schedule_report = NO_CLASSES_CALENDAR_LECTURER_MESSAGE.format(
                datetime.strptime(date_code, '%Y%m%d').strftime('%d-%m-%Y'), lecturer_url
            )
        elif today:
            schedule_report = NO_CLASSES_TODAY_LECTURER_MESSAGE.format(lecturer_url)
        else:
            schedule_report = NO_CLASSES_TOMORROW_LECTURER_MESSAGE.format(lecturer_url)
    else:
        date = lecturer_data['date'].split()

        schedule_report = f'👩‍🏫 <b>{lecturer_name}</b>\n\n' \
            f'📌 <u><b>{DAY_CONVERT_DICT[date[0]]}</b> {date[-1]}</u>\n\n'

        for i in range(len(lecturer_data['order'])):
            for header in ['order', 'time', 'subject', 'group', 'room', 'free_rooms']:
                if header == 'order':
                    schedule_report += f'{ORDER_CONVERT_DICT[lecturer_data[header][i]]}\n'
                elif header == 'room':
                    schedule_report += (f'{CONVERT_TABLE_HEADERS[header]} '
                                        f'{find_building_location(lecturer_data[header][i])}\n')
                elif header == 'free_rooms':
                    if lecturer_data[header][i]:
                        schedule_report += f'<a href="{lecturer_data[header][i]}" title="свободные аудитории">' \
                                  f'<b>{CONVERT_TABLE_HEADERS[header]}</b></a>\n'
                else:
                    schedule_report += f'{CONVERT_TABLE_HEADERS[header]} {lecturer_data[header][i]}\n'

            schedule_report += '\n'

        schedule_report += f'🚀 <a href="{lecturer_url}" title="расписание"><b>Расписание на текущую неделю</b></a>'

    return schedule_report
