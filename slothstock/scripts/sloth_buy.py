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

import numpy
import pandas
from tqdm import tqdm

from slothstock import __version__
from slothstock import constants
from slothstock import exceptions
from slothstock import utils
from slothstock.indicators import macd_indicator
from slothstock.providers.xueqiu import XueQiu


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--token')
    parser.add_argument('--filter-st', action='store_false')
    parser.add_argument('--filter-suspend', action='store_false')
    parser.add_argument('--topic-ids', action='append', default=[])
    parser.add_argument('--uids', action='append', default=[])
    parser.add_argument('-e', '--ebk', action='append', default=[])
    parser.add_argument('-i', '--interval', default=1, type=int)
    parser.add_argument('-o', '--output', default='sloth.ebk')
    parser.add_argument('-p', '--period', default='day')
    parser.add_argument('-s', '--strict', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    return parser.parse_args()


def load_stocks(ebk):
    """Load symbols."""
    stocks_ashare = XueQiu.list_ashare()
    stocks_etf = XueQiu.list_etf()
    stocks = pandas.concat([stocks_ashare, stocks_etf], sort=False)

    if ebk:
        res = set()
        for filename in ebk:
            res.update(utils.import_ebk(filename))
        stocks = stocks[stocks.index.isin(res)]

    return stocks


def check_buy(stocks, args):
    """Check buy signals."""
    res = set()
    idx = constants.PERIODS.index(args.period)
    symbols = stocks.sample(frac=1).index

    pbar = tqdm(symbols)
    for symbol in pbar:
        pbar.set_description(symbol)

        # Filter ST stocks.
        if args.filter_st and 'name' in stocks.columns and \
                'ST' in stocks.loc[symbol, 'name']:
            continue

        # Filter suspended stocks.
        if args.filter_suspend and 'volume' in stocks.columns and \
                numpy.isnan(stocks.loc[symbol, 'volume']):
            continue

        # Check great-great-grandparent period.
        if args.strict:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx + 4]
            kline = XueQiu.kline(symbol, period_cur)
            _, _, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_expand_golden_cross(macdhist):
                continue

        # Check grandparent period.
        time.sleep(args.interval)
        period_cur = constants.PERIODS[idx + 2]
        kline = XueQiu.kline(symbol, period_cur)
        _, _, macdhist = macd_indicator.clean_macd(kline.close)
        if not macd_indicator.is_expand_golden_cross(macdhist):
            continue

        # Check current period.
        time.sleep(args.interval)
        kline = XueQiu.kline(symbol, args.period)
        macd, macdsignal, macdhist = macd_indicator.clean_macd(kline.close)
        if not macd_indicator.is_negative(macd, macdsignal, args.strict):
            continue
        if not macd_indicator.is_about_to_golden_cross(macdhist, args.strict):
            continue

        # Check child period.
        if args.strict:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx - 1]
            kline = XueQiu.kline(symbol, period_cur)
            macd, macdsignal, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_negative(macd, macdsignal, args.strict):
                continue
            if not macd_indicator.is_about_to_bottom_divergence(
                    macd, macdsignal, macd_indicator, args.strict):
                continue

        res.add(symbol)
    return stocks[stocks.index.isin(res)].sort_index()


def main():
    """Indicate buy signals."""
    args = parse_args()

    if args.period not in constants.PERIODS_VALID:
        raise exceptions.InvalidPeriodError()

    stocks = load_stocks(args.ebk)
    stocks = check_buy(stocks, args)
    title = f'{args.period}级别可能买点'
    if stocks.index.empty:
        title = f'{args.period}级别无可能买点'
    print(title)
    print(stocks)
    utils.export_ebk(stocks.index, args.output)
    utils.send_notification(
        stocks, title, args.token, args.topic_ids, args.uids)


if __name__ == '__main__':
    main()
