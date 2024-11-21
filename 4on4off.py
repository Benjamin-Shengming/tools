#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta

def is_on_shift(start_date, check_date):
    # Create datetime objects from the input integers
    # Calculate the number of days between the given date and the start date
    days_difference = (check_date - start_date).days
    
    # Determine if the given date is an 'on' or 'off' shift
    return (days_difference % 8) < 4

def show_result(d, res): 
    res_txt = "On" if res else "Off" 
    print(f"{d.strftime('%Y-%m-%d')} is: {res_txt}")

def check_all_dates(s, e):
    res = []
    check_date = s
    while(check_date <= e): 
        res.append((check_date, is_on_shift(s, check_date)))
        check_date += timedelta(days=1)
    return res
        
        
def parse_args(): 
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    parser = argparse.ArgumentParser(description="Determine if a given date is an 'on' or 'off' work shift based on a 4 on 4 off schedule.")
    
    parser.add_argument('--start_year', type=int, default=2024, help='Start year')
    parser.add_argument('--start_month', type=int, default=12, help='Start month')
    parser.add_argument('--start_day', type=int, default=2, help='Start day')
    
    parser.add_argument('--check_year', type=int, default=current_year, help='Check year')
    parser.add_argument('--check_month', type=int, default=current_month, help='Check month')
    parser.add_argument('--check_day', type=int, default=current_day, help='Check day')
    parser.add_argument('--check_all', type=bool, default=True, help='Check all days from start date to the check date inclusive')
    
    args = parser.parse_args()

    start_date = datetime(args.start_year, args.start_month, args.start_day)
    check_date = datetime(args.check_year, args.check_month, args.check_day)
    if (start_date > check_date): 
        raise  RuntimeError(f"Check date {check_date.strftime('%Y-%m-%d')}  is before start date {start_date.strftime('%Y-%m-%d')}")
    return start_date, check_date, args.check_all

    
def main():
    try:
        start_date, end_date, check_all = parse_args();    
        if check_all: 
            res = check_all_dates(start_date, end_date)
            for d, r in res:
                show_result(d, r)
        else:
            res = is_on_shift(start_date, end_date)
            show_result(end_date, res)

    except Exception as e: 
        print(e)

if __name__ == "__main__":
    main()




