#!/usr/bin/env python3

import pandas as pd
from search_util import *

records = load_excel("2024.xlsx")

def total_paid(records): 
    total = 0
    for x in records:
        paid_str = x["amount Paid"] 
        if not paid_str:
            continue
        paid = int(paid_str)
        total += paid
    return total

def paid_to_count(amount):
    if amount == 12:
        return 1 
    if amount == 17: 
        return 2
    elif amount == 20: 
        return 2
    elif amount ==24:
        return 2 
    if (amount % 5) != 0:
        print(amount)
        raise RuntimeError("Wrong amount")
    return amount // 5

def count_member(records): 
    total = 0
    for x in records:
        paid_str = x["amount Paid"] 
        if not paid_str:
            continue
        paid = int(paid_str)
        total += paid_to_count(paid)
    return total


print(count_member(records))
print(total_paid(records))