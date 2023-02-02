import datetime
from collections import defaultdict
import json
import pickle
import jsonpickle



class hourSheet:
    def __init__(self):
        month_dictionaries = [defaultdict(dict) for x in range(12)]
        self.__list_days = {str(month+1): dictionary for month, dictionary in enumerate(month_dictionaries)}

    def start_today(self, time:int):
        day_now, month_now = self.get_todays_day_and_month()
        self.start_day(time=time,day=day_now, month=month_now)

    def end_today(self, time:int):
        day_now, month_now = self.get_todays_day_and_month()
        self.end_day(time=time,day=day_now, month=month_now)

    def get_todays_day_and_month(self):
        day_now = datetime.datetime.now().day
        month_now = datetime.datetime.now().month
        return day_now,month_now

    def start_day(self, time:int, day:int, month:int):
        current_day_start_time = self.transform_time_as_ints_to_datetime(
            time, day, month
        )
        self.insert_new_entry_for_current_day(current_day_start_time, "start")

    def end_day(self, time, day, month):
        current_day_end_time = self.transform_time_as_ints_to_datetime(
            time, day, month
        )
        self.insert_new_entry_for_current_day(current_day_end_time, "end")

    def __transform_timedelta_to_int(self, hours_worked):
        return hours_worked.total_seconds() / 3600

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

    def add_full_workday(self, date, month, start_time, end_time):
        self.start_day(start_time, date, month)
        self.end_day(end_time, date, month)
                

    def get_most_recent_hoursheet_entry(self) -> dict:
        return self.__list_days[str(datetime.datetime.now().month)][str(datetime.datetime.now().day)]

    def list_days(self):
        return self.__list_days

    def get_workday(self, day: int, month: int):
        return self.__list_days[str(month)][str(day)]

    def transform_time_as_ints_to_datetime(
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

###### STATISTICS SECTION ######

    def get_summary_for_date(self, day, month):
        workday = self.get_workday(day, month)
        hours_worked_as_timedelta = workday["end"] - workday["start"]
        return self.__transform_timedelta_to_int(hours_worked_as_timedelta)

    def get_week_summary_given_date(self, date, month):
        this_year = datetime.datetime.now().year
        date_datetime = datetime.datetime(this_year, month, date)
        _, week_number, week_day  = date_datetime.isocalendar()
        day_of_week = date_datetime - datetime.timedelta(week_day-1)
        total_hours = 0
        while day_of_week.isocalendar().week == week_number:
            if self.get_workday(day_of_week.day, day_of_week.month):
                total_hours += self.get_summary_for_date(day=day_of_week.day, month=day_of_week.month)
            day_of_week += datetime.timedelta(1)
        return total_hours

    def get_current_week_summary(self):
        day_now, month_now = self.get_todays_day_and_month()
        return self.get_week_summary_given_date(date=day_now, month=month_now)
        
        

##### IO SECTION #####



    def save_hour_sheet(self, filename:str):
        with open(filename, mode="wb") as external_file_storage:
            pickle.dump(self, external_file_storage)

    def save_json(self, filename:str):
        with open(file=filename, mode="w") as json_file:
            hour_sheet_json = jsonpickle.encode(self)
            json_file.write(hour_sheet_json)
    
    @staticmethod
    def from_binary_file(filename:str):
        with open(filename, mode="rb") as external_file_storage:
            hour_sheet = pickle.load(external_file_storage)
            return hour_sheet
    
    @staticmethod
    def from_text_file(filename:str):
        with open(filename, mode="r") as external_file_storage:
            hour_sheet_from_txt = hourSheet()
            for line in external_file_storage:
                line = line.strip()
                line = line.split(" ")
                line[0] = line[0].strip(":")
                start_time, end_time = line[1].split("-")
                start_time = start_time.lstrip("0")
                date, month = line[0].split("/")
                hour_sheet_from_txt.add_full_workday(int(date), int(month), int(start_time), int(end_time))
            return hour_sheet_from_txt
    
    @classmethod
    def from_JSON(cls, filename:str):
        with open(filename, mode="r", encoding="cp1257") as external_file:
            hour_sheet_string = external_file.read()
            hour_sheet_obj = jsonpickle.decode(hour_sheet_string)
            # hour_sheet_obj = jsonpickle.decode(hour_sheet_obj)
            return hour_sheet_obj
