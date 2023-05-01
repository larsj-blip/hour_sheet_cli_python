import json
from dataclasses import field, dataclass
import datetime
from typing import Optional


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