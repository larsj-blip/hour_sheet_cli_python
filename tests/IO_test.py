from pathlib import Path
from unittest.mock import patch

from assertpy import assert_that

from src.hour_sheet import HourSheet

ALL_MONTHS = [str(month+1) for month in range(12)]


def create_test_file_path():
    global TEST_FILE_NAME
    if Path.cwd().name == "hour_sheet":
        return Path(Path.cwd(), "tests", "resources", "test_file")
    return Path(Path.cwd(), "resources", "test_file")


TEST_FILE_NAME = create_test_file_path()


def should_save_file_as_json_file_independent_of_class_structure(hour_sheet_with_full_workday):
    populated_hour_sheet = hour_sheet_with_full_workday
    populated_hour_sheet.save(TEST_FILE_NAME.with_suffix(".json"))
    with open(TEST_FILE_NAME.with_suffix(".json"), "r") as hour_sheet_file:
        hour_sheet_str_list = hour_sheet_file.readlines()
        hour_sheet_str = "".join(hour_sheet_str_list)
        assert_that(hour_sheet_str).is_not_empty()
        assert_that(hour_sheet_str).contains(*ALL_MONTHS)

def should_convert_hour_sheet_to_json_compatible_dictionary(hour_sheet_with_full_workweek):
    hour_sheet = hour_sheet_with_full_workweek
    jsondict = hour_sheet.to_dict()
    assert_that(jsondict).is_instance_of(dict)
    assert_that(jsondict).is_not_empty()




def should_load_file_from_json_representation():
    hour_sheet = HourSheet.from_json(str(TEST_FILE_NAME.with_suffix(".json")))
    assert_that(hour_sheet).is_instance_of(HourSheet)
    assert_that(hour_sheet.all_data()).is_not_empty()

@patch('src.hour_sheet.HourSheet.save')
def should_save_file_after_exiting_context(mock_save):
    hour_sheet = HourSheet(filename=str(TEST_FILE_NAME))
    with hour_sheet:
        hour_sheet.start_today(800)
    HourSheet.save.assert_called()



    