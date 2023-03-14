DEFAULT_FILE = "timeliste_2023_tru.json"

from hour_sheet import hourSheet


def add_entry_to_hoursheet(hoursheet, args, file=DEFAULT_FILE):
    hour_sheet = hoursheet.from_json(file)
    with hour_sheet:
        if args.entry_type == "start":
            hour_sheet.start_today(args.time)
        elif args.entry_type == "stop":
            hour_sheet.end_today(args.time)
