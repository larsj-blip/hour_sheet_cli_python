

import datetime

from assertpy import assert_that


CURRENT_DAY = datetime.datetime.now().day
CURRENT_MONTH = datetime.datetime.now().month
START_TIME_AS_INT = 800
END_TIME_AS_INT = 1800


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


def should_calculate_how_many_hours_need_to_be_worked_to_work_a_full_week():
    pass

def should_show_graphical_representation_of_hours_worked():
    pass

# def should_create_summary_of_hours_for_week_number(hour_sheet_with_full_workday):
#     hour_sheet = hour_sheet_with_full_workday
#     week_number = 51
#     hours_worked_in_a_given_week = hour_sheet.get_week_summary(week_number)
#     assert_that(hours_worked_in_a_given_week).is_equal_to(8)