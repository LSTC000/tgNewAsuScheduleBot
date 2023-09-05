from data.config import DAY_CONVERT_DICT, ORDER_CONVERT_DICT, CONVERT_TABLE_HEADERS

from data.messages import NO_CLASSES_WEEKLY_STUDENT_MESSAGE

from .find_building_location import find_building_location


def create_student_weekly_schedule_report(
    student_name: str,
    student_url: str,
    weekly_student_data: list,
    no_classes: bool
) -> list:
    """
    :param student_name: Student name.
    :param student_url: Url to the weekly student schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param weekly_student_data: Contains the dicts: key - the name of the table header and the value - the header data.
    :param no_classes: True - student don`t has a classes on week, else - False.
    :return: List with student daily schedule report.
    """

    weekly_schedule_report = []

    if no_classes:
        weekly_schedule_report.append(NO_CLASSES_WEEKLY_STUDENT_MESSAGE.format(student_url))
    else:
        weekly_schedule_report.append(f'👨‍🎓 <b>{student_name}</b>\n\n')

        for student_data in weekly_student_data:
            date = student_data['date'].split()
            schedule_report = f'📌 <u><b>{DAY_CONVERT_DICT[date[0]]}</b> {date[-1]}</u>\n\n'

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

            weekly_schedule_report.append(schedule_report)

    return weekly_schedule_report
