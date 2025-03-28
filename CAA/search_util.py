#!/usr/bin/env python3

import pandas as pd

from pprint import pprint
from loguru import logger

CN = 'Chinese Name'
CNS = 'Chinese Name(Spouse)'
MNO = "Number"
MONEY="amount Paid"
HEADCNT="Financial Member count"


def excel_to_df(file_path=None):
    df = pd.read_excel(file_path).fillna("")
    return df 

def df_to_excel(df, file_path=None):
    df.to_excel(file_path, index=False)

def dicts_from_df(df):
    records_list_of_dict = df.to_dict(orient='records')
    for x in records_list_of_dict:
        if x[MNO]:
            try:
                x[MNO] = int(x[MNO]) 
            except: 
                print(f"not a number detected {x[MNO]}")
    recs = remove_empty_rows(records_list_of_dict)
    return recs

def df_from_dicts(list_dicts): 
    return pd.DataFrame(list_dicts)


def load_excel(file_path=None):
    df = pd.read_excel(file_path).fillna("")
    #df[HEADCNT].replace([''], '0', inplace=True)
    df.replace({HEADCNT: ''}, '0', inplace=True)

    df[HEADCNT] = df[HEADCNT].astype('uint8')
    records_list_of_dict = df.to_dict(orient='records')
    for x in records_list_of_dict:
        if x[MNO]:
            try:
                x[MNO] = int(x[MNO]) 
            except: 
                print(f"not a number detected {x[MNO]}")
    recs = remove_empty_rows(records_list_of_dict)
    return recs 

def to_excel(mem_list, file_path):
    excel_rec = [x.data for x in mem_list]
    excel_pd = pd.DataFrame(excel_rec)
    excel_pd.to_excel(file_path)

def remove_empty_rows(recs):
    ret = []
    for x in recs: 
        for _, v in x.items():
           if v: 
               ret.append(x) 
               break 
    return ret

def money_to_headcnt(amount):
    if amount == 12:
        return 1 
    if amount == 17: 
        return 2
    elif amount == 20: 
        return 3
    elif amount ==24:
        return 2 
    assert (amount % 5) == 0, f"Wrong amount {amount}"
    return amount // 5


class MemberInfo():
    def __init__(self, rec):
        self.info = rec 
        assert self.info[MNO], "Member number is empty" + str(self.info)


    def has_mno(self):
        if self.NO:
            return int(self.NO)
        else:
            return False


    def has_paid(self):
        return self.amount > 0 

    def update_heads_count_with_paidamount(self):
        if not self.has_paid():
            return 
        if self.heads_count > 0:
            return
        self.info[HEADCNT] = money_to_headcnt(self.amount)

    @property
    def heads_count(self):
        try:
            return int(self.info[HEADCNT])
        except:
            return 0


    @property
    def NO(self):
        return self.info[MNO]

    @property
    def cn_cns(self):
        if not self.cns:
            return set([self.cn]) 
        elif "，" in self.cns:
            ret = set([self.cn])
            cns_names = [x for x in self.cns.split("，")]
            for x in cns_names:
                x = x.strip()
                if x:
                    ret.add(x)
            logger.debug(len(ret))
            logger.debug(ret)
            return ret
        elif "," in self.cns:
            ret = set([self.cn])
            cns_names = [x for x in self.cns.split(",")]
            for x in cns_names:
                x = x.strip()
                if x:
                    ret.add(x)
            logger.debug(len(ret))
            logger.debug(ret)
            return ret
        else:
            return set([self.cn, self.cns])

    @property
    def cn(self):
        return self.info[CN]


    @property
    def cns(self):
        return self.info[CNS]

    @property
    def amount(self):
        if self.info[MONEY]:
            return int(self.info[MONEY])
        else:
            return 0

    @property
    def data(self):
        return self.info

    

def check_amount_names_headscnt(m):
    money_heads = money_to_headcnt(m.amount)
    logger.debug(f"money_heads {money_heads}") 

    logger.debug(f"input heads {m.heads_count}") 

    return len(set([int(money_heads), 
                    int(m.heads_count)])) == 1


def wrong_amount_names_headscnt(m):
    return not check_amount_names_headscnt(m)
    

def to_meminfo_list(rec): 
    return [MemberInfo(x) for x in rec]

def to_dicts_list(m_list):
    return [x.info for x in m_list]

def list_mem_vi_no(mno, m_list):
    return list(filter(lambda x: str(x.NO) == str(mno), m_list))


def list_mem_paid(m_list): 
    ret = []
    for x in m_list:
        if x.has_paid():
            ret.append(x)
    return ret


def list_mem_unpaid(m_list): 
    ret = []
    for x in m_list:
        if not x.has_paid():
            ret.append(x)
    return ret


def match_member_no(member_no, records):
    ret = [] 
    for x in records:
        if x[MNO] == member_no: 
           ret.append(x) 
    return ret 

def match_chinese_name_exact(name, records):
    member_name = name.lower()
    ret = []
    for x in records:
        if ( 
         member_name in x[CN].lower() or
         member_name in x[CNS].lower()
        ):
            ret.append(x)
    return ret


def get_duplicates_numbers(records):
    mem_nos = [int(item[MNO]) for item in records if item[MNO]] 
    dups = [item for item, count in collections.Counter(mem_nos).items() if count > 1]
    return dups 


def extract_dict_fields(r, keys):
    ret = {} 
    for k in keys: 
        if k in r.keys(): 
            ret[k] = r[k]
        else:
            ret[k] = None
    return ret


def extract_fields(records, keys):
    ret = []
    for x in records: 
        ret.append(extract_dict_fields(x, keys))
    return ret


def check_money_values(amount):
    if amount in [0, 5, 10, 12, 17, 20, 24]: 
        return True
    else:
        return amount % 5 == 0

