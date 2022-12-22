import datetime
import os
from assertpy import assert_that
from src.hour_sheet import hourSheet
import pytest

CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1800
TEST_FILE_NAME = "test_file"



def should_save_start_time_for_workday_from_int_representations_of_date_and_time(
    temp_hour_sheet_with_start_date,
):
    temp_hour_sheet = temp_hour_sheet_with_start_date
    list_of_days = temp_hour_sheet.most_recent_day()
    assert_that(list_of_days).is_not_empty()

# def should_not_create_start_or_end_of_workday_if_it_already_exists_for_specified_date(temp_hour_sheet_with_start_date):
#     hour_sheet = temp_hour_sheet_with_start_date
#     assert_that(hour_sheet.start_day(START_TIME_AS_INT, CURRENT_DAY, CURRENT_MONTH)).raises(RuntimeError)

def should_save_end_of_workday_object_together_with_start_of_workday_object(
    hour_sheet_with_full_workday
):
    temp_hour_sheet = hour_sheet_with_full_workday
    most_recent_day = temp_hour_sheet.most_recent_day()
    assert_that(most_recent_day).contains_key("start")
    assert_that(most_recent_day).contains_key("end")

def should_differentiate_between_workdays_from_different_months(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    new_month = (CURRENT_MONTH+1)%12
    hour_sheet.start_day(900, CURRENT_DAY, new_month)
    hour_sheet.end_day(1700, CURRENT_DAY, new_month)
    assert_that(len(hour_sheet.list_days())).is_greater_than(1)

def should_return_summary_of_hours_worked_for_a_given_date_as_int(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    hour_summary_as_int = hour_sheet.get_summary_for_date(CURRENT_DAY, CURRENT_MONTH) #CHANGE ORDER
    assert_that(hour_summary_as_int).is_equal_to(10)

def should_save_summary_to_file_in_the_project_root_directory_with_input_as_name(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    hour_sheet.save_hour_sheet(TEST_FILE_NAME)
    assert_that(TEST_FILE_NAME).exists()

def should_load_hour_sheet_object_from_binary_file():
    loaded_hour_sheet = hourSheet.from_binary_file(TEST_FILE_NAME)
    assert_that(loaded_hour_sheet).is_instance_of(hourSheet)


def should_create_summary_of_hours_for_week_given_date_within_that_week(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    date = CURRENT_DAY
    month = CURRENT_MONTH
    hours_worked_in_week = hour_sheet.get_week_summary_given_date(date, month)
    assert_that(hours_worked_in_week).is_equal_to(10)

def should_show_graphical_representation_of_hours_worked():
    pass
def should_save_file_as_txt_file_independent_of_class_structure():
    pass
def should_calculate_how_many_hours_need_to_be_worked_to_work_a_full_week():
    pass



# def should_create_summary_of_hours_for_week_number(hour_sheet_with_full_workday):
#     hour_sheet = hour_sheet_with_full_workday
#     week_number = 51
#     hours_worked_in_a_given_week = hour_sheet.get_week_summary(week_number)
#     assert_that(hours_worked_in_a_given_week).is_equal_to(8)

# def should_parse_text_file_and_create_hour_sheet_object_from_text_file():
#     loaded_hour_sheet = hourSheet.from_text_file("timer.txt")
#     assert_that(loaded_hour_sheet).is_instance_of(hourSheet)


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
