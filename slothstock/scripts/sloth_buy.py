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

from slothstock import constants
from slothstock import utils
from slothstock.indicators import macd_indicator
from slothstock.providers import XueQiu
from slothstock.scripts import common
from slothstock.scripts import parsers


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser(parents=[
        parsers.BUY_PARSER,
        parsers.MISC_PARSER,
        parsers.SLOTHSTOCK_PARSER,
        parsers.WXPUSHER_PARSER,
    ])
    return parser.parse_args()


def check_buy(stocks, args):
    """Check buy signals."""
    symbols = stocks.sample(frac=1).index
    idx = constants.PERIODS.index(args.period)
    candidate_buy = set()

    pbar = tqdm(symbols, disable=args.daemon)
    for symbol in pbar:
        pbar.set_description(symbol)

        # Whether to reserve ST stocks.
        if not args.reserve_st and utils.is_st(stocks.loc[symbol]):
            continue

        # Whether to reserve suspended stocks.
        if not args.reserve_suspend and utils.is_suspend(stocks.loc[symbol]):
            continue

        # Check great-great-grandparent period.
        if idx + 4 < len(constants.PERIODS) and \
                args.check_great_great_grandparent:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx + 4]
            kline = XueQiu.kline(symbol, period_cur)
            _, _, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_golden_cross(macdhist, args.loose):
                continue

        # Check grandparent period.
        if idx + 2 < len(constants.PERIODS):
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx + 2]
            kline = XueQiu.kline(symbol, period_cur)
            _, _, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_golden_cross(macdhist, args.loose):
                continue

        # Check current period.
        time.sleep(args.interval)
        kline = XueQiu.kline(symbol, args.period)
        macd, macdsignal, macdhist = macd_indicator.clean_macd(kline.close)
        if not macd_indicator.is_negative(macd, macdsignal, args.loose):
            continue
        if not macd_indicator.is_about_to_golden_cross(macdhist, args.loose):
            continue

        # Check child period.
        if idx > 0 and not args.skip_child:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx - 1]
            kline = XueQiu.kline(symbol, period_cur)
            macd, macdsignal, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_about_to_bottom_divergence(
                    macd, macdsignal, macd_indicator, args.loose):
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
