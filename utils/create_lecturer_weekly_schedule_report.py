from data.config import DAY_CONVERT_DICT, ORDER_CONVERT_DICT, CONVERT_TABLE_HEADERS

from data.messages import NO_CLASSES_WEEKLY_LECTURER_MESSAGE

from .find_building_location import find_building_location


def create_lecturer_weekly_schedule_report(
    lecturer_name: str,
    lecturer_url: str,
    weekly_lecturer_data: list,
    no_classes: bool
) -> list:
    """
    :param lecturer_name: Lecturer name.
    :param lecturer_url: Url to the weekly lecturer schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param weekly_lecturer_data: Contains the dicts: key - the name of the table header and the value - the header data.
    :param no_classes: True - lecturer don`t has a classes on week, else - False.
    :return: List with student daily schedule report.
    """

    weekly_schedule_report = []

    if no_classes:
        weekly_schedule_report.append(NO_CLASSES_WEEKLY_LECTURER_MESSAGE.format(lecturer_url))
    else:
        weekly_schedule_report.append(f'👩‍🏫 <b>{lecturer_name}</b>\n\n')

        for lecturer_data in weekly_lecturer_data:
            date = lecturer_data['date'].split()
            schedule_report = f'📌 <u><b>{DAY_CONVERT_DICT[date[0]]}</b> {date[-1]}</u>\n\n'

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

            weekly_schedule_report.append(schedule_report)

    return weekly_schedule_report
