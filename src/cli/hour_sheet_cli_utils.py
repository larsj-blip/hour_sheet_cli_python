DEFAULT_FILE = "timeliste_2023_tru.json"



def add_entry_to_hoursheet(args, hour_sheet):
    with hour_sheet:
        if args.entry_type == "start":
            hour_sheet.start_today(args.time)
        elif args.entry_type == "stop":
            hour_sheet.end_today(args.time)
