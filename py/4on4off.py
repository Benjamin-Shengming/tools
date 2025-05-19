#!/usr/bin/env python3

import argparse
import calendar
import holidays
from datetime import datetime, timedelta
from humanfriendly.terminal import ansi_wrap

act_holidays = holidays.Australia(state="ACT")


def red(i):
    return ansi_wrap(i, color="red")


def grn(i):
    return ansi_wrap(i, color="green")


def blue(i):
    return ansi_wrap(i, color="blue")


def white(i):
    return ansi_wrap(i, color="white")


def yellow(i):
    return ansi_wrap(i, color="yellow")


def is_weekend(d):
    return d.weekday() >= 5


def is_holiday(d):
    is_holiday = True if d in act_holidays else False


def date_str(d):
    return d.strftime("%Y-%m-%d")


def cl(d, is_on):
    d_str = d.strftime("%Y-%m-%d")
    day_str = str(d.day)
    if (is_holiday(d) or is_weekend(d)) and is_on:
        return blue(d_str), blue(day_str), blue("On")
    elif is_on:
        return red(d_str), red(day_str), red("Off")
    else:
        return white(d_str), white(day_str), white("Off")


def is_on_shift(start_date, check_date):
    # Create datetime objects from the input integers
    # Calculate the number of days between the given date and the start date
    days_difference = (check_date - start_date).days

    # Determine if the given date is an 'on' or 'off' shift
    return (days_difference % 8) < 4


def show_mark_days(year, month, days):
    print()
    # Create a TextCalendar instance
    cal = calendar.TextCalendar(firstweekday=0)

    # Get the month's calendar as a list of weeks
    month_calendar = cal.monthdayscalendar(year, month)

    print(f"    {yellow(calendar.month_name[month])} {yellow(str(year))}")
    print(f'{"Mo":<5}{"Tu":<5}{"We":<5}{"Th":<5}{"Fr":<5}{"Sa":<5}{"Su":<5}')
    # Print the calendar with the marked days
    for week in month_calendar:
        for day in week:
            if day == 0:
                print(f'{" ":<5}', end="")
            else:
                _, d_str, _ = cl(
                    datetime(year, month, day), True if day in days else False
                )
                print(f"{d_str:<14}", end="")
        print()
    print()


def show_list(date_list):
    for d in date_list:
        d_t, _, txt = cl(d[0], True)
        print(f"{d_t} is: {txt}")


def show_calendar(date_list):
    # build this dict structure
    # {
    #    year(int): {
    #        month(int):[days]
    #
    #    }
    # }
    last_year = date_list[-1][0].year
    last_month = date_list[-1][0].month
    last_day = date_list[-1][0].day

    c_dict = {}
    for d in date_list:
        if not d[1]:
            continue
        yr = d[0].year
        mo = d[0].month
        day = d[0].day
        if yr not in c_dict.keys():
            c_dict[yr] = {}
        yr_dict = c_dict[yr]
        if mo not in yr_dict.keys():
            yr_dict[mo] = []
        yr_dict[mo].append(day)
    for y, m_dict in c_dict.items():
        for m, d_list in m_dict.items():
            if (yr == last_year) and (mo == last_month):
                show_mark_days(y, m, d_list)
            else:
                show_mark_days(y, m, d_list)


def check_all_dates(s, e):
    res = []
    check_date = s
    while check_date <= e:
        res.append((check_date, is_on_shift(s, check_date)))
        check_date += timedelta(days=1)
    return res


def parse_args():
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    parser = argparse.ArgumentParser(
        description="Determine if a given date is an 'on' or 'off' work shift based on a 4 on 4 off schedule."
    )

    parser.add_argument(
        "--start_year", type=int, default=2024, help="Start year"
    )
    parser.add_argument(
        "--start_month", type=int, default=12, help="Start month"
    )
    parser.add_argument("--start_day", type=int, default=2, help="Start day")

    parser.add_argument(
        "--end_year", type=int, default=current_year, help="Check year"
    )
    parser.add_argument(
        "--end_month", type=int, default=current_month, help="Check month"
    )
    parser.add_argument(
        "--end_day", type=int, default=current_day, help="Check day"
    )
    parser.add_argument(
        "--one_day",
        action="store_true",
        default=False,
        help="check on day only",
    )
    parser.add_argument(
        "--show_list",
        action="store_true",
        default=False,
        help="show as calendar format",
    )

    args = parser.parse_args()

    start_date = datetime(args.start_year, args.start_month, args.start_day)
    end_date = datetime(args.end_year, args.end_month, args.end_day)
    if start_date > end_date:
        raise RuntimeError(
            f"End date {end_date.strftime('%Y-%m-%d')}  is before start date {start_date.strftime('%Y-%m-%d')}"
        )
    args.start_date = start_date
    args.end_date = end_date
    return args


def main():
    try:
        args = parse_args()
        res = []
        if not args.one_day:
            res = check_all_dates(args.start_date, args.end_date)
        else:
            res = [(args.end_date, is_on_shift(args.start_date, args.end_date))]

        sorted_dates = sorted(res, key=lambda x: x[1])

        if not args.show_list:
            show_calendar(res)
        else:
            show_list(res)

    except Exception as e:
        print(e)
        raise e


if __name__ == "__main__":
    main()
