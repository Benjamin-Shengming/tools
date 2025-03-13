#!/usr/bin/env python3

import pandas as pd
from search_util import *

mem_name = input("Enter an membership name: ")

def has_name(name, records):
    member_name = name.lower()
    ret = []
    for x in records:
        try:
            if (member_name in x[CN]):
                ret.append(x)
        except:
            print(x)
    return ret

def match_member_name(name, records):
    member_name = name.lower()
    ret = []
    for x in records:
        try:
            if ( member_name in x['FirstName'].lower() or 
            member_name in x['Surname'].lower() or
            member_name in x[CN].lower() or
            member_name in x[CNS].lower() or
            member_name in x['Family Spouse Name'].lower()
            ):
                ret.append(x)
        except:
            print(x)
    return ret


print("name in 2021:")
same_names= has_name(mem_name, rec21)
for x in same_names:
    print(x)
    
print("name in 2022:")
same_names= has_name(mem_name, rec22)
for x in same_names:
    print(x)

print("name in 2023:")
same_names= has_name(mem_name, rec23)
for x in same_names:
    print(x)


print("name in 2024:")
same_names= has_name(mem_name, rec24)
for x in same_names:
    print(x)
