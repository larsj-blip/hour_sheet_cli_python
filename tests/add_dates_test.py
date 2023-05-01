from __future__ import annotations
from assertpy import assert_that

from .conftest import CURRENT_DAY, CURRENT_MONTH


class AddDatesTest:
    @staticmethod
    def should_not_implicitly_overwrite_existing_entry(temp_hour_sheet_with_start_date):
        hour_sheet = temp_hour_sheet_with_start_date
        hour_sheet.end_day(1600, CURRENT_DAY, CURRENT_MONTH)
        expected_hour_summary = hour_sheet.get_summary_for_date(day=CURRENT_DAY, month=CURRENT_MONTH)
        hour_sheet.start_day(1800, day=CURRENT_DAY, month=CURRENT_MONTH)
        assert_that(hour_sheet.get_summary_for_date(CURRENT_DAY, CURRENT_MONTH)).is_equal_to(expected_hour_summary)

    @staticmethod
    def should_not_end_workday_that_does_not_have_start():
        pass

    @staticmethod
    def should_not_add_workday_if_no_hours_were_registered_previous_weekday():
        pass
