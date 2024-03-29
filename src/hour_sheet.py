from dataclasses import dataclass, field
import datetime
from collections import defaultdict
import json
from typing import Optional

CURRENT_YEAR = datetime.date.year
DEFAULT_FILE_NAME = f"timeliste_json_ish_for_år_{CURRENT_YEAR}.json"


@dataclass
class WorkDay:
    start: datetime.datetime = field(init=False, default=None)
    end: Optional[datetime.datetime] = field(init=False, default=None)

    def start_day(self, date: datetime.datetime):
        if not self.start:
            self.start = date
        else:
            # TODO: raise error?
            print("entry exists, should use update function")

    def end_day(self, date: datetime.datetime):
        if not self.end:
            self.end = date
        else:
            # TODO: raise error?
            print("entry exists, should use update function")

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        worksheet_dictionary = {"start": self.start.isoformat()}
        if self.end:
            worksheet_dictionary["end"] = self.end.isoformat()
        return worksheet_dictionary
    @staticmethod
    def from_dict(workday_as_dict):
        workday = WorkDay()
        if "start" in workday_as_dict:
            workday.start = datetime.datetime.fromisoformat(workday_as_dict.get("start"))
        if "end" in workday_as_dict:
            workday.end = datetime.datetime.fromisoformat(workday_as_dict.get("end"))
        return workday


class HourSheet:

    def __init__(self, filename=DEFAULT_FILE_NAME):
        month_dictionaries = [defaultdict(WorkDay) for _ in range(12)]
        self.__all_months_containing_workdays = {str(month + 1): dictionary for month, dictionary in
                                                 enumerate(month_dictionaries)}
        self.filename = filename

    def start_today(self, time: int):
        day_now, month_now = self.get_todays_day_and_month()
        self.start_day(time=time, day=day_now, month=month_now)

    def end_today(self, time: int):
        day_now, month_now = self.get_todays_day_and_month()
        self.end_day(time=time, day=day_now, month=month_now)

    @staticmethod
    def get_todays_day_and_month():
        day_now = datetime.datetime.now().day
        month_now = datetime.datetime.now().month
        return day_now, month_now

    def start_day(self, time: int, day: int, month: int):
        current_day_start_time = self.transform_time_as_ints_to_datetime(
            time, day, month
        )
        self.insert_new_start_day_entry(current_day_start_time)

    def end_day(self, time, day, month):
        current_day_end_time = self.transform_time_as_ints_to_datetime(
            time, day, month
        )
        self.insert_new_end_day_entry(current_day_end_time)

    def insert_new_end_day_entry(self, current_day: datetime.datetime):
        workday = self.fetch_existing_or_create_new_workday(current_day)
        workday.end_day(current_day)
        self.__all_months_containing_workdays[str(current_day.month)][str(current_day.day)] = workday

    def insert_new_start_day_entry(self, current_day: datetime.datetime):
        workday = self.fetch_existing_or_create_new_workday(current_day)
        workday.start_day(current_day)
        self.__all_months_containing_workdays[str(current_day.month)][str(current_day.day)] = workday

    def fetch_existing_or_create_new_workday(self, current_day):
        key_for_current_day = str(current_day.day)
        key_for_current_month = str(current_day.month)
        all_data = self.all_data()
        month = all_data.get(key_for_current_month)
        workday = month.get(key_for_current_day, WorkDay())
        return workday

    @staticmethod
    def __transform_timedelta_to_int(hours_worked):
        return hours_worked.total_seconds() / 3600

    def add_full_workday(self, date, month, start_time, end_time):
        self.start_day(start_time, date, month)
        self.end_day(end_time, date, month)

    def all_data(self):
        return self.__all_months_containing_workdays

    def get_workday(self, day: int, month: int):
        return self.__all_months_containing_workdays.get(str(month)).get(str(day))

    @staticmethod
    def transform_time_as_ints_to_datetime(time_as_int, current_day_as_int, current_month_as_int) -> datetime.datetime:
        time_in_hours_as_int = time_as_int // 100
        time_in_minutes_as_int = time_as_int - time_in_hours_as_int * 100
        start_time_for_current_day = datetime.datetime(
            2022,
            current_month_as_int,
            current_day_as_int,
            time_in_hours_as_int,
            time_in_minutes_as_int,
        )
        return start_time_for_current_day

    def __enter__(self):
        return self

    def __exit__(self, type_var, value, tb):
        self.save(self.filename)

    @staticmethod
    def is_valid_date_entry(entry: WorkDay):
        if entry.start and entry.end:
            return True
        return False

    # STATISTICS SECTION

    def get_summary_for_date(self, day, month):
        workday = self.get_workday(day, month)
        hours_worked_as_timedelta = workday.end - workday.start
        return self.__transform_timedelta_to_int(hours_worked_as_timedelta)

    def get_week_summary_given_date(self, date, month):
        this_year = datetime.datetime.now().year
        date_datetime = datetime.datetime(this_year, month, date)
        _, week_number, week_day = date_datetime.isocalendar()
        day_of_week = date_datetime - datetime.timedelta(week_day - 1)
        total_hours = 0
        while day_of_week.isocalendar().week == week_number:
            workday = self.get_workday(day_of_week.day, day_of_week.month)
            if workday and workday.start and workday.end:
                total_hours += self.get_summary_for_date(day=day_of_week.day, month=day_of_week.month)
            day_of_week += datetime.timedelta(1)
        return total_hours

    def get_current_week_summary(self):
        day_now, month_now = self.get_todays_day_and_month()
        return self.get_week_summary_given_date(date=day_now, month=month_now)

    def get_summary_given_iso_week(self, week_number):
        this_year = datetime.datetime.now().year
        day_in_week = datetime.datetime.fromisocalendar(this_year, week_number, day=1)
        total_hours = 0
        while day_in_week.isocalendar().week == week_number:
            if self.get_workday(day_in_week.day, day_in_week.month):
                total_hours += self.get_summary_for_date(day=day_in_week.day, month=day_in_week.month)
            day_in_week += datetime.timedelta(1)
        return total_hours

    # def get_invalid_entries_in_month(self, month: str) -> list:
    #     month_of_entries = self.all_data().get(month)
    #     invalid_days = [date for date, workday in month_of_entries.items() if self.is_valid_date_entry(workday)]
    #     return invalid_days

    # IO SECTION

    def to_dict(self):
        year_dictionary = {}
        for month, month_values in self.__all_months_containing_workdays.items():
            month_dictionary = {}
            for day, day_values in month_values.items():
                day_dict = day_values.to_dict()
                month_dictionary[day] = day_dict
            year_dictionary[month] = month_dictionary
        return year_dictionary

    def save(self, filename):
        with open(file=filename, mode="w") as file:
            hour_sheet = self.to_dict()
            json.dump(hour_sheet, fp=file)

    @classmethod
    def from_json(cls, filename: str):
        with open(filename, mode="r", encoding="utf-8") as external_file:
            hour_sheet = HourSheet(filename=filename)
            hour_sheet_string = "".join(external_file.readlines())
            all_months_list = json.loads(hour_sheet_string)
            all_months = {month: cls.create_hour_sheet_objects_for_month(month_dict) for month, month_dict in
                          all_months_list.items()}
            hour_sheet.__all_months_containing_workdays = all_months
            return hour_sheet

    @classmethod
    def create_hour_sheet_objects_for_month(cls, year_dict):
        month_dict = {}
        for day, day_values in year_dict.items():
            month_dict[day] = WorkDay.from_dict(day_values)
        return month_dict
