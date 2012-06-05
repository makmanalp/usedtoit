"""
The tracker is intentionally kept to a minimum of functionality. It is a thin
wrapper that writes a data value for a date in a yaml file.
"""
import argparse
import os
import time
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc

DATADIR = "~/.usedtoit/"
DATAEXT = ".yml"

if __name__ == "__main__":

    """
    Sample invocations would be:

        tracker pullups 5 --date "2 days ago"
        tracker junkfood 1
     """
    parser = argparse.ArgumentParser(description="Form new habits by tracking and reinforcing them.")
    parser.add_argument("calendar_name", action="store")
    parser.add_argument("value", action="store", type=int)
    parser.add_argument("--date", action="store", dest="value_date", default=time.time())
    args = parser.parse_args()

    """
    The data is stored in the `~/.usedtoit/` directory by default. If you have
    `yoga.yml` in there, `yoga` will be one of your calendars. Just `touch` a new
    file in the data directory to create a new calendar.
    """
    calendars = {}
    for root,dirs,files in os.walk(DATADIR):
        for file_name in [f for f in files if f.endswith(DATAEXT)]:
            raw_name = file_name[:-4]
            calendars[raw_name] = root + file_name

    if args.calendar_name not in calendars:
        raise Exception("Calendar '%s' does not exist. Calendars found: %s" % (args.calendar_name, calendars) )

    """
    The date is parsed intelligently w/ `parsedatetime` so you can type in
    humanized dates like "2 days ago".  It is stored in a human-readable and
    editable format as opposted to a unix timestamp, in case you'd want to edit
    the file yourself.
    """
    date_parser = pdt.Calendar(pdc.Constants())
    parsed_date = time.gmtime(time.mktime(date_parser.parse(args.value_date)))
    string_date = time.strftime("%Y-%m-%d %H:%M:%S", parsed_date[0])

    with open(calendars[args.calendar_name], "a+") as f:
        f.write("%s: %s %s" % (string_date, args.value, os.linesep))
