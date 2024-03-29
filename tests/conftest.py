import datetime
import pytest
from src.hour_sheet import HourSheet

CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1830
EXPECTED_WORK_WEEK_HOURS = 52.5
EXPECTED_WORK_DAY_HOURS = 10.5
TEST_FILE_NAME = "test_file"


@pytest.fixture
def hour_sheet_with_full_workweek():
    hour_sheet = HourSheet()
    current_weeks_monday = get_current_weeks_monday()
    for x in range(5):
        hour_sheet.start_day(START_TIME_AS_INT, current_weeks_monday.day, current_weeks_monday.month)
        hour_sheet.end_day(END_TIME_AS_INT, current_weeks_monday.day, current_weeks_monday.month)
        current_weeks_monday += datetime.timedelta(days=1)
    return hour_sheet


@pytest.fixture
def workweek_with_missing_end_time():
    hour_sheet = HourSheet()
    current_weeks_monday = get_current_weeks_monday()
    for x in range(5):
        hour_sheet.start_day(START_TIME_AS_INT, current_weeks_monday.day, current_weeks_monday.month)
        current_weeks_monday += datetime.timedelta(days=1)
    return hour_sheet


@pytest.fixture
def hour_sheet_with_full_workday(temp_hour_sheet_with_start_date):
    hour_sheet = temp_hour_sheet_with_start_date
    hour_sheet.end_today(END_TIME_AS_INT)
    return hour_sheet


@pytest.fixture
def temp_hour_sheet_with_start_date():
    hour_sheet = HourSheet()
    hour_sheet.start_today(START_TIME_AS_INT)
    return hour_sheet


def get_current_weeks_monday():
    today = datetime.datetime.now()
    weekday = today.weekday()
    monday = today - datetime.timedelta(days=weekday - 1)
    return monday
