SCHEDULE_ASU_URL = 'https://www.asu.ru/timetable/'

STUDENT_SCHEDULE_URL = 'https://www.asu.ru/timetable/students/{}'
LECTURER_SCHEDULE_URL = 'https://www.asu.ru/timetable/lecturers/{}'

JSON_STUDENTS_SCHEDULE_QUERY_URL = 'https://www.asu.ru/timetable/search/students/?query={}&file=list.json&api_token={}'
JSON_LECTURERS_SCHEDULE_QUERY_URL = 'https://www.asu.ru/timetable/search/lecturers/?query={}&file=list.json&api_token={}'
JSON_WEEKLY_SCHEDULE_URL = '{}?file=list.json&api_token={}'
JSON_DATE_QUERY_URL = '{}?date={}&file=list.json&api_token={}'

FREE_ROOMS_URL_DICT = {
    'a': 'https://www.asu.ru/timetable/freerooms/?date={}&building=1',
    'д': 'https://www.asu.ru/timetable/freerooms/?date={}&building=2',
    'к': 'https://www.asu.ru/timetable/freerooms/?date={}&building=3',
    'л': 'https://www.asu.ru/timetable/freerooms/?date={}&building=4',
    'м': 'https://www.asu.ru/timetable/freerooms/?date={}&building=5',
    'н': 'https://www.asu.ru/timetable/freerooms/?date={}&building=6',
    'с': 'https://www.asu.ru/timetable/freerooms/?date={}&building=7',
    'э': 'https://www.asu.ru/timetable/freerooms/?date={}&building=8',
    'я': 'https://www.asu.ru/timetable/freerooms/?date={}&building=9'
}
