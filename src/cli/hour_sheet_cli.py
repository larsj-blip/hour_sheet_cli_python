import argparse
from dataclasses import dataclass
from src.cli.hour_sheet_cli_utils import add_entry_to_hoursheet



parser = argparse.ArgumentParser(description="helloooooo creating cli should I be testing cli? how to test...")
parser.add_argument("--entry-type", choices=["start", "stop"])
parser.add_argument("--time", type=int)
args = parser.parse_args()


add_entry_to_hoursheet(args)
