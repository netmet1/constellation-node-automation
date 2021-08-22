import pytz
import argparse

def retrieve_arguments():
    tz_search = argparse.ArgumentParser(description="quick search Python TimeZones")

    tz_search.add_argument("-s", "--search", 
                            metavar='search_word',
                            type=str,
                            default=False,
                            help="Search for timezone based on full or partial search entry.")

    tz_search.add_argument("-a", "--all", help="print out all timezones",
                            action="store_true", default=False)

    return tz_search.parse_args()

if __name__ == "__main__":
    tz_args = retrieve_arguments()

    for tz in pytz.all_timezones:
        if tz_args.all:
            print(tz)
        elif tz_args.search:
            if tz_args.search in tz:
                print(tz)