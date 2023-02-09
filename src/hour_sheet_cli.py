import argparse

from .hour_sheet import hourSheet

parser = argparse.ArgumentParser(description="helloooooo creating cli should I be testing cli? how to test...")
parser.add_argument("time as int",metavar="time", type=int, nargs=1)
parser.add_argument("--start-today", dest="")
parser.add_argument("--end-today")