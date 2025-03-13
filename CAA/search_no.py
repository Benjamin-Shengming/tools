#!/usr/bin/env python3

import pandas as pd
from search_util import *

member_no = int(input("Enter an membership no: "))
records = load_excel("2024.xlsx")



same_members = match_member_no(member_no, records)
for x in same_members:
    print(x[MNO], x[CN])