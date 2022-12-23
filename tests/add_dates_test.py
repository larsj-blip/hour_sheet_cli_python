
from assertpy import assert_that
from src.hour_sheet import hourSheet
import datetime



CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1800




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








