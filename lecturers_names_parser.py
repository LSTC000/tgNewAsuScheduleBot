import json
import time

from data.config import REQUEST_HEADERS, JSON_TOKEN

import requests


json_url = '{}?file=list.json&api_token={}'
lecturers_url = 'https://www.asu.ru/timetable/lecturers/'
lecturer_list = []

response = requests.get(url=json_url.format(lecturers_url, JSON_TOKEN), headers=REQUEST_HEADERS)
time.sleep(1)

data = response.json()
faculties_records = data['faculties']['records']

for faculties_record in faculties_records:
    print(f'[-----Faculty: {faculties_record["facultyTitle"]}-----]')
    faculty_url = lecturers_url + str(faculties_record['facultyId'])
    response = requests.get(url=json_url.format(faculty_url, JSON_TOKEN), headers=REQUEST_HEADERS)
    time.sleep(1)

    data = response.json()
    chairs_records = data['chairs']['records']

    for chairs_record in chairs_records:
        print(f'[Chair: {chairs_record["chairTitle"]}]')
        chair_url = faculty_url + '/' + str(chairs_record['chairId'])
        response = requests.get(url=json_url.format(chair_url, JSON_TOKEN), headers=REQUEST_HEADERS)
        time.sleep(1)

        data = response.json()
        lecturers_records = data['lecturers']['records']

        for lecturers_record in lecturers_records:
            lecturer_name = lecturers_record['lecturerName']
            print(f'Lecturer: {lecturer_name}')
            lecturer_list.append(lecturer_name)

with open('lecturers_names.json', 'w', encoding='utf-8') as file:
    json.dump({'lecturers_names': lecturer_list}, file, indent=4, ensure_ascii=False)
