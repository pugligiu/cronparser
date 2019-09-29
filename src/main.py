#!/usr/bin/python3

from cronparser import CronParser
import sys

if __name__ == "__main__":
    arg = " ".join(sys.argv[1:])
    p = CronParser(arg)
    p.print_cron_table()
