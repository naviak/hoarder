from datetime import datetime


def is_digit_str(s):
    return all(c.isdigit() for c in s)


def get_today_data():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')
