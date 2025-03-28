#!/usr/bin/env python3

from argparse import ArgumentParser 
import pandas as pd
from search_util import *
import sys

def single_true(iterable):
    i = iter(iterable)
    return any(i) and not any(i)


def total_amount(m_list):
    total = 0
    for m in m_list:
        if not m.has_paid():
            continue 
        total += m.amount
    return total


def show_mem_list(mem_list, title="need to check"): 
    if not mem_list:
        logger.info("==== All good ====")
    else:
        logger.info(f"\n\n {title}")
        for x in mem_list:
            logger.info(x.data)
    logger.info("\n\n")


def show_mem_list_brv(mem_list, title="need to check"):
    if not mem_list:
        logger.info("==== All good ====")
    else:
        logger.info(f"\n\n {title}")
        for x in mem_list:
            d = extract_dict_fields(x.data, [MNO, CN, CNS, MONEY, HEADCNT])
            logger.info(d)
    logger.info("\n\n")



def detect_empty_member_no(mem_list):
    logger.info("===Check empty member number!===")
    ret = []
    for x in mem_list:
        if x.has_mno():
            continue
        ret.append(x)
    show_mem_list(ret, "No member number")

def detect_amount_paid_value(mem_list):
    logger.info("===Check all member paid the valid values!===")
    invalid_paid = []
    for x in mem_list:
        if check_money_values(x.amount):
            continue
        invalid_paid.append(x)
    show_mem_list_brv(invalid_paid, "invalid amount")

def detect_amount_headscnt_names(mem_list): 
    logger.info("===Check Invalid amount, names, heads count!===")
    mem_list = list_mem_paid(mem_list)
    ret = list(filter(lambda x: wrong_amount_names_headscnt(x), mem_list))
    show_mem_list_brv(ret, "amount, names and head count does not match!")


def audit(args): 
    all_rec = load_excel(args.input)
    mem_list = to_meminfo_list(all_rec)
    if args.mno:
        mem_list = list_mem_vi_no(args.mno, mem_list)
    
    detect_empty_member_no(mem_list)
    detect_amount_paid_value(mem_list)
    detect_amount_headscnt_names(mem_list)


    logger.info(f"\n\nTotal Amount:  {total_amount(mem_list)}")


def auto_fill(args):
    df = excel_to_df(args.input)
    mem_list = to_meminfo_list(dicts_from_df(df))
    for x in mem_list:
        x.update_heads_count_with_paidamount()
    updated_dicts = to_dicts_list(mem_list) 
    new_df = df_from_dicts(updated_dicts)
    if not args.output: 
        args.output = "./tmp.xlsx"
    df_to_excel(new_df, args.output)


def search_name(args):
    pass

def search_no(args):
    pass

def search(args):
    pass

def parse_args():
    parser = ArgumentParser(
        description="Command Interface Member")

    parser.add_argument("--list-unpaid", action="store_true", default=False,
                        help="list unpaid members")

    parser.add_argument("--audit", action="store_true", default=False,
                        help="audit")

    parser.add_argument("--search", action="store_true", default=False,
                        help="search name or number")

    parser.add_argument("--auto-fill", action="store_true", default=False,
                        help="auto fill information")

    parser.add_argument(
        "--mno", default=None, help="only analyze one member"
    )
    parser.add_argument(
        "--input", default="./2025.xlsx", help="input excel file"
    )
    parser.add_argument(
        "--output", default=None, help="output file"
    )
    parser.add_argument(
        "--debug", action="store_true", default=False, help="debug"
    )

    args = parser.parse_args()

    assert single_true(
        (   args.list_unpaid,
            args.audit,
            args.auto_fill,
            args.search,
        )
    ), "Please use one command only"
    return args


def dispatch_to_cmd(args):
    if args.debug:
        logger.remove() 
        logger.add(sys.stdout, level="DEBUG")
    if args.list_unpaid:
        list_unpaid(args)
    if args.auto_fill:
        auto_fill(args)
    if args.search:
       search(args)
    else:
       audit(args)


def main():
    try:
        args = parse_args()
        dispatch_to_cmd(args)
    except AssertionError as e:
        logger.error(e.args[0])


if __name__ == "__main__":
    main()




