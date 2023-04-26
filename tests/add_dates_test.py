from __future__ import annotations
from assertpy import assert_that
from src.hour_sheet import HourSheet
import datetime

from .conftest import CURRENT_DAY, CURRENT_MONTH


def should_not_implicitly_overwrite_existing_entry_(temp_hour_sheet_with_start_date):
    hour_sheet = temp_hour_sheet_with_start_date
    hour_sheet.end_day(1600, CURRENT_DAY, CURRENT_MONTH)
    expected_hour_summary = hour_sheet.get_summary_for_date(day=CURRENT_DAY, month=CURRENT_MONTH)
    hour_sheet.start_day(1800, day=CURRENT_DAY, month=CURRENT_MONTH)
    assert_that(hour_sheet.get_summary_for_date(CURRENT_DAY, CURRENT_MONTH)).is_equal_to(expected_hour_summary)


def should_differentiate_between_workdays_from_different_months(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    new_month = (CURRENT_MONTH + 1) % 12
    hour_sheet.start_day(900, CURRENT_DAY, new_month)
    hour_sheet.end_day(1700, CURRENT_DAY, new_month)
    assert_that(len(hour_sheet.all_data())).is_greater_than(1)


def should_not_end_workday_that_does_not_have_start():
    pass


def should_not_add_workday_if_no_hours_were_registered_previous_weekday():
    pass
