import datetime
import pytest
from src.hour_sheet import hourSheet


CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1800
TEST_FILE_NAME = "test_file"



@pytest.fixture
def hour_sheet_with_full_workday(end_time_as_int, temp_hour_sheet_with_start_date):
    temp_hour_sheet = temp_hour_sheet_with_start_date
    temp_hour_sheet.end_day(end_time_as_int, CURRENT_DAY, CURRENT_MONTH)
    return temp_hour_sheet


@pytest.fixture
def temp_hour_sheet_with_start_date(start_time_as_int):
    temp_hour_sheet = hourSheet()
    start_time_as_int = start_time_as_int
    temp_hour_sheet.start_day(start_time_as_int, CURRENT_DAY, CURRENT_MONTH)
    return temp_hour_sheet


@pytest.fixture
def start_time_as_int():
    time_as_int = START_TIME_AS_INT
    return time_as_int


@pytest.fixture
def end_time_as_int():
    time_as_int = END_TIME_AS_INT
    return time_as_int



