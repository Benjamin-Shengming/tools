#!/usr/bin/env python3

import pandas as pd
from search_util import *

records = load_excel("2024.xlsx")
plan_to_add = load_excel("new.xlsx")


def same_no_and_name(r1, r2):
    pass

def same_no(r1, r2):
    pass

def same_chinese_name(r1, r2):
    if set(r1['Chinese Name'].lower(), r1['Chinese Name(Spouse)'].lower()).intersection(
       set(r2['Chinese Name'].lower(), r2['Chinese Name(Spouse)'].lower())    
    ):
        return True
    return False

def match_old_member(new_x, records): 

    # name, member are exactly same 
    matched = match_chinese_name_exact(new_x, records) 
    return matched 


def update_old_member(new_x):
    pass 

for new_x in plan_to_add:
    # member no is there and name is same and not paid yet, 
    old_member = match_old_member(new_x)
    if len(old_member) >= 2: 
        print(old_member)
        raise RuntimeError("more than 2 matched")
    old_member 
    update_old_member(new_x)




