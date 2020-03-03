#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script indicating sell signals.

File: sloth_sell.py
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


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[
            parsers.MISC_PARSER,
            parsers.SELL_PARSER,
            parsers.SLOTHSTOCK_PARSER,
            parsers.WXPUSHER_PARSER,
        ],
    )
    return parser.parse_args()


def check_sell(stocks, args):
    """Check sell signals."""
    symbols = stocks.sample(frac=1).index
    idx = PERIODS.index(args.period)
    candidate_sell = set()

    pbar = tqdm(symbols, disable=args.daemon)
    for symbol in pbar:
        pbar.set_description(symbol)

        # Check parent period.
        if idx + 1 < len(PERIODS) and args.check_parent:
            time.sleep(args.interval)
            kline = XueQiu.kline(symbol, PERIODS[idx + 1], args.datetime)
            macd = MACD(kline.close)
            if not macd.golden or (not args.loose and not macd.narrow):
                continue

        # Check current period.
        time.sleep(args.interval)
        kline = XueQiu.kline(symbol, args.period, args.datetime)
        macd = MACD(kline.close)
        if not macd.golden or (not args.loose and not macd.narrow):
            continue

        # Check child period.
        if idx > 0 and args.child:
            time.sleep(args.interval)
            kline = XueQiu.kline(symbol, PERIODS[idx - 1], args.datetime)
            macd = MACD(kline.close)
            if args.child == CHILD_CHOICE_CROSS:
                if not macd.golden or (not args.loose and not macd.narrow):
                    continue
            elif not macd.will_top_divergence:
                continue

        candidate_sell.add(symbol)
    return stocks[stocks.index.isin(candidate_sell)].sort_index()


def main():
    """Indicate sell signals."""
    args = parse_args()

    stocks = XueQiu.list_stocks(args.ebk)
    stocks = check_sell(stocks, args)
    common.show_result(stocks, '卖', args)


if __name__ == '__main__':
    main()
