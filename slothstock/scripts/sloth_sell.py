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

from slothstock import constants
from slothstock.indicators import macd_indicator
from slothstock.providers import XueQiu
from slothstock.scripts import common
from slothstock.scripts import parsers


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser(parents=[
        parsers.MISC_PARSER,
        parsers.SLOTHSTOCK_PARSER,
        parsers.WXPUSHER_PARSER,
    ])
    return parser.parse_args()


def check_sell(stocks, args):
    """Check sell signals."""
    symbols = stocks.sample(frac=1).index
    idx = constants.PERIODS.index(args.period)
    candidate_sell = set()

    pbar = tqdm(symbols, disable=args.daemon)
    for symbol in pbar:
        pbar.set_description(symbol)

        # Check current period.
        time.sleep(args.interval)
        kline = XueQiu.kline(symbol, args.period)
        _, _, macdhist = macd_indicator.clean_macd(kline.close)
        if not macd_indicator.is_about_to_death_cross(macdhist, args.loose):
            continue

        # Check child period.
        if idx > 0 and not args.skip_child:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx - 1]
            kline = XueQiu.kline(symbol, period_cur)
            _, _, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_about_to_death_cross(
                    macdhist, args.loose):
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
