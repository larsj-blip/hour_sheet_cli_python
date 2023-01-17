

import datetime

from assertpy import assert_that


CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1800
TOTAL_HOURS_FOR_ONE_WORKWEEK = 50


def should_return_summary_of_hours_worked_for_a_given_date_as_int(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    hour_summary_as_int = hour_sheet.get_summary_for_date(CURRENT_DAY, CURRENT_MONTH) #CHANGE ORDER
    assert_that(hour_summary_as_int).is_equal_to(10)


def should_create_summary_of_hours_for_week_given_date_within_that_week(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    date = CURRENT_DAY
    month = CURRENT_MONTH
    hours_worked_in_week = hour_sheet.get_week_summary_given_date(date, month)
    assert_that(hours_worked_in_week).is_equal_to(10)

def should_show_how_many_hours_worked_in_current_week(hour_sheet_with_full_workweek):
    hour_sheet = hour_sheet_with_full_workweek
    hours_worked_current_week = hour_sheet.get_current_week_summary()
    assert_that(hours_worked_current_week).is_equal_to(TOTAL_HOURS_FOR_ONE_WORKWEEK)

def should_calculate_how_many_hours_remain_get_to_a_full_work_week():
    pass

def should_show_graphical_representation_of_hours_worked():
    pass

# def should_create_summary_of_hours_for_week_number(hour_sheet_with_full_workday):
#     hour_sheet = hour_sheet_with_full_workday
#     week_number = 51
#     hours_worked_in_a_given_week = hour_sheet.get_week_summary(week_number)
#     assert_that(hours_worked_in_a_given_week).is_equal_to(8)