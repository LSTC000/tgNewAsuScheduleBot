import datetime


def get_date_codes() -> tuple:
    '''
    :return: Today and tomorrow query url code.
        Example: today: '20230326', tomorrow: '20230327'.
    '''

    today_date = datetime.date.today()
    tomorrow_date = today_date + datetime.timedelta(days=1)

    return today_date.strftime('%Y%m%d'), tomorrow_date.strftime('%Y%m%d')
