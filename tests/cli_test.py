# from dataclasses import dataclass
# from unittest.mock import patch
# from assertpy import assert_that
# from src.cli import hour_sheet_cli_utils
# from src.hour_sheet import hourSheet
# from tests.IO_test import TEST_FILE_NAME

# START_TIME = 900

# @dataclass
# class mock_namespace:
#     entry_type: str
#     time: int

# @patch.object(src.hour_sheet.hourSheet, "start_today")
# def should_start_day_given_command_line_args_with_start_flag_and_int_corresponding_to_time(mocked_hoursheet):
#     start_day_input = mock_namespace(entry_type="start", time=START_TIME)
#     hour_sheet_cli_utils.add_entry_to_hoursheet(mocked_hoursheet, start_day_input, TEST_FILE_NAME)
#     mocked_hoursheet.start_today.assert_called_with(START_TIME)
    