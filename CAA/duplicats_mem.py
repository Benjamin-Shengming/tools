#!/usr/bin/env python3

import collections

from search_util import *
records = load_excel("2024.xlsx")
mem_nos = [int(item[MNO]) for item in records if item[MNO]] 
dups = [item for item, count in collections.Counter(mem_nos).items() if count > 1]

for x in records:
    mem_no = x[MNO]
    if mem_no in dups: 
        print(x[MNO], x[CN])