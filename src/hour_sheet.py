import datetime
from collections import defaultdict
import json
import pickle
import jsonpickle

from src.hour_sheet_encoder import HourSheetEncoder


class hourSheet:
    def __init__(self):
        month_dictionaries = [defaultdict(dict) for x in range(12)]
        self.__list_days = {str(month+1): dictionary for month, dictionary in enumerate(month_dictionaries)}

    def start_day(self, time_as_int, current_day_as_int, current_month_as_int):
        current_day_start_time = self.transform_time_as_int_to_datetime(
            time_as_int, current_day_as_int, current_month_as_int
        )
        self.insert_new_entry_for_current_day(current_day_start_time, "start")

    def end_day(self, time_as_int, current_day_as_int, current_month_as_int):
        current_day_end_time = self.transform_time_as_int_to_datetime(
            time_as_int, current_day_as_int, current_month_as_int
        )
        self.insert_new_entry_for_current_day(current_day_end_time, "end")

    def get_summary_for_date(self, day, month):
        workday = self.get_workday(day, month)
        hours_worked_as_timedelta = workday["end"] - workday["start"]
        return self.__transform_timedelta_to_hours(hours_worked_as_timedelta)

    def __transform_timedelta_to_hours(self, hours_worked):
        return hours_worked.total_seconds() // 3600

    def insert_new_entry_for_current_day(
        self, current_day: datetime.datetime, entry_type: str
    ):
        key_for_current_day = str(current_day.day)
        key_for_current_month = str(current_day.month)
        if entry_type in self.list_days()[key_for_current_month][key_for_current_day]:
            print("This date already exists. To overwrite, use the overwrite function.")
        else:
            workday_dictionary = {entry_type: current_day}
            self.__list_days[key_for_current_month][key_for_current_day].update(
                workday_dictionary
            )

    def save_hour_sheet(self, filename:str):
        with open(filename, mode="wb") as external_file_storage:
            pickle.dump(self, external_file_storage)

    def save_json(self, filename:str):
        with open(file=filename, mode="w") as json_file:
            hour_sheet_json = jsonpickle.encode(self)
            json_file.write(hour_sheet_json)
    
    @classmethod
    def from_binary_file(cls, filename:str):
        with open(filename, mode="rb") as external_file_storage:
            hour_sheet = pickle.load(external_file_storage)
            return hour_sheet
    
    @classmethod
    def from_text_file(cls, filename:str):
        with open(filename, mode="r") as external_file_storage:
            hour_sheet = cls
            for line in external_file_storage:
                line = line.strip()
                line = line.split(" ")
                line[0] = line[0].strip(":")
                start_time, end_time = line[1].split("-")
                start_time = start_time.lstrip("0")
                date, month = line[0].split("/")
                hour_sheet.add_full_workday(int(date), int(month), int(start_time), int(end_time))
            return hour_sheet
    
    @classmethod
    def from_JSON(cls, filename:str):
        with open(filename, mode="r", encoding="cp1257") as external_file:
            hour_sheet_string = external_file.read()
            hour_sheet_obj = jsonpickle.decode(hour_sheet_string)
            # hour_sheet_obj = jsonpickle.decode(hour_sheet_obj)
            return hour_sheet_obj

    def add_full_workday(self, date, month, start_time, end_time):
        self.start_day(start_time, date, month)
        self.end_day(end_time, date, month)
                

    def get_week_summary_given_date(self, date, month):
        this_year = datetime.datetime.now().year
        week_number = datetime.datetime(this_year, month, date).isocalendar()[1]
        total_hours = 0
        for date in self.__list_days[str(month)]:
            workday = self.get_workday(date, month)
            if workday["start"].isocalendar()[1] == week_number:
                total_hours += self.get_summary_for_date(date, month)
        return total_hours

    def most_recent_day(self) -> dict:
        return self.__list_days[str(datetime.datetime.now().month)][str(datetime.datetime.now().day)]

    def list_days(self):
        return self.__list_days

    def get_workday(self, day: int, month: int):
        return self.__list_days[str(month)][str(day)]

    def transform_time_as_int_to_datetime(
        self, time_as_int, current_day_as_int, current_month_as_int
    ) -> datetime.datetime:
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
