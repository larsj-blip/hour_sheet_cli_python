import argparse
from dataclasses import dataclass

from .hour_sheet import hourSheet
DEFAULT_FILE = "timeliste_2023_tru.json"



parser = argparse.ArgumentParser(description="helloooooo creating cli should I be testing cli? how to test...")
parser.add_argument("--entry-type", choices=["start", "stop"])
parser.add_argument("--time", type=int)
args = parser.parse_args()


hour_sheet = hourSheet.from_json(DEFAULT_FILE)
with hour_sheet:
    if args.entry_type == "start":
        hour_sheet.start_today(args.time)
    hour_sheet.end_today(args.time)

