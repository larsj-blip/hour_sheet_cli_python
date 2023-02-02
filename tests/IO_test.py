import datetime
import json
import os
import sys
from pathlib import Path
import pytest

import chardet
from assertpy import assert_that

from src.hour_sheet import hourSheet

ALL_MONTHS = [str(month+1) for month in range(12)]
TEST_FILE_NAME = Path("./tests/resources/test_file")


def should_save_summary_to_file_in_the_project_root_directory_with_input_as_name(hour_sheet_with_full_workday):
    hour_sheet = hour_sheet_with_full_workday
    hour_sheet.save_hour_sheet(str(TEST_FILE_NAME))
    assert_that(str(TEST_FILE_NAME)).exists()

def should_load_hour_sheet_object_from_binary_file():
    loaded_hour_sheet = hourSheet.from_binary_file(TEST_FILE_NAME)
    assert_that(loaded_hour_sheet).is_instance_of(hourSheet)


def should_parse_text_file_and_create_hour_sheet_object_from_text_file():
    loaded_hour_sheet = hourSheet.from_text_file(TEST_FILE_NAME.with_suffix(".txt"))
    assert_that(loaded_hour_sheet).is_instance_of(hourSheet)

def should_save_file_as_json_file_independent_of_class_structure(hour_sheet_with_full_workday):
    populated_hour_sheet = hour_sheet_with_full_workday
    populated_hour_sheet.save_json(TEST_FILE_NAME.with_suffix(".json"))
    with open(TEST_FILE_NAME.with_suffix(".json"), "r") as hour_sheet_file:
        hour_sheet_str_list = hour_sheet_file.readlines()
        hour_sheet_str = "".join(hour_sheet_str_list)
        assert_that(hour_sheet_str).is_not_empty()
        assert_that(hour_sheet_str).contains(*ALL_MONTHS)

def should_load_file_from_json_representation():
    hour_sheet = hourSheet.from_JSON(TEST_FILE_NAME.with_suffix(".json"))
    assert_that(hour_sheet).is_instance_of(hourSheet)
    assert_that(hour_sheet.list_days()).is_not_empty()

def should_save_hoursheet_using_default_name_containing_year():
    hour_sheet = hourSheet()
    hour_sheet.save()
    assert_that(Path(""))



    