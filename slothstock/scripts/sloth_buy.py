#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script indicating buy signals.

File: sloth_buy.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse
import time

from tqdm import tqdm

from slothstock.constants import CHILD_CHOICE_CROSS
from slothstock.constants import PERIODS
from slothstock.indicators import MACD
from slothstock.providers import XueQiu
from slothstock.scripts import common
from slothstock.scripts import parsers
from slothstock.utils import is_st
from slothstock.utils import is_suspend


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[
            parsers.BUY_PARSER,
            parsers.MISC_PARSER,
            parsers.SLOTHSTOCK_PARSER,
            parsers.WXPUSHER_PARSER,
        ],
    )
    return parser.parse_args()


def check_buy(stocks, args):
    """Check buy signals."""
    symbols = stocks.sample(frac=1).index
    idx = PERIODS.index(args.period)
    candidate_buy = set()

    pbar = tqdm(symbols, disable=args.daemon)
    for symbol in pbar:
        pbar.set_description(symbol)

        # Whether to reserve ST stocks.
        if not args.reserve_st and is_st(stocks.loc[symbol]):
            continue

        # Whether to reserve suspended stocks.
        if not args.reserve_suspend and is_suspend(stocks.loc[symbol]):
            continue

        # Check great-great-grandparent period.
        if idx + 4 < len(PERIODS) and \
                args.check_great_great_grandparent:
            time.sleep(args.interval)
            kline = XueQiu.kline(symbol, PERIODS[idx + 4], args.datetime)
            macd = MACD(kline.close)
            if not macd.golden or (not args.loose and not macd.expand):
                continue

        # Check grandparent period.
        if idx + 2 < len(PERIODS):
            time.sleep(args.interval)
            kline = XueQiu.kline(symbol, PERIODS[idx + 2], args.datetime)
            macd = MACD(kline.close)
            if not macd.golden or (not args.loose and not macd.expand):
                continue

        # Check current period.
        time.sleep(args.interval)
        kline = XueQiu.kline(symbol, args.period, args.datetime)
        macd = MACD(kline.close)
        if not macd.negative or not macd.death or \
                (not args.loose and not macd.narrow):
            continue

        # Check child period.
        if idx > 0 and args.child:
            time.sleep(args.interval)
            kline = XueQiu.kline(symbol, PERIODS[idx - 1], args.datetime)
            macd = MACD(kline.close)
            if args.child == CHILD_CHOICE_CROSS:
                if not macd.death or (not args.loose and not macd.narrow):
                    continue
            elif not macd.will_bottom_divergence:
                continue

        candidate_buy.add(symbol)
    return stocks[stocks.index.isin(candidate_buy)].sort_index()


def main():
    """Indicate buy signals."""
    args = parse_args()

    stocks = XueQiu.list_stocks(args.ebk)
    stocks = check_buy(stocks, args)
    common.show_result(stocks, '买', args)


if __name__ == '__main__':
    main()
