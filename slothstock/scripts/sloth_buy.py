#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script indicating buy signals.

File: sloth_buy.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse
from datetime import datetime
from datetime import timedelta
import time

from tqdm import tqdm

from slothstock import constants
from slothstock import exceptions
from slothstock import parsers
from slothstock import utils
from slothstock.indicators import macd_indicator
from slothstock.providers import XueQiu


def parse_args():
    """Argument Parser."""
    parser = argparse.ArgumentParser(parents=[
        parsers.MISC_PARSER,
        parsers.SLOTHSTOCK_PARSER,
        parsers.WXPUSHER_PARSER,
    ])
    return parser.parse_args()


def check_buy(stocks, args):
    """Check buy signals."""
    res = set()
    idx = constants.PERIODS.index(args.period)
    symbols = stocks.sample(frac=1).index

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
        if args.great_great_grandparent_period:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx + 4]
            kline = XueQiu.kline(symbol, period_cur)
            _, _, macdhist = macd_indicator.clean_macd(kline.close)
            if not macd_indicator.is_golden_cross(macdhist, args.strict):
                continue

        # Check grandparent period.
        time.sleep(args.interval)
        period_cur = constants.PERIODS[idx + 2]
        kline = XueQiu.kline(symbol, period_cur)
        _, _, macdhist = macd_indicator.clean_macd(kline.close)
        if not macd_indicator.is_golden_cross(macdhist, args.strict):
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
        if args.child_period:
            time.sleep(args.interval)
            period_cur = constants.PERIODS[idx - 1]
            kline = XueQiu.kline(symbol, period_cur)
            macd, macdsignal, macdhist = macd_indicator.clean_macd(kline.close)
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

    stocks = XueQiu.list_stocks(args.ebk)
    stocks = check_buy(stocks, args)

    utils.export_ebk(stocks.index, args.output)

    title = args.title
    if not title:
        title = f'{args.period}级别可能买点'
        if stocks.index.empty:
            title = f'{args.period}级别无可能买点'

    content = [title]
    content.extend([
        f'{symbol} {stocks.loc[symbol, "name"]}'
        for symbol in stocks.index
    ])
    content.append(str(datetime.utcnow() + timedelta(hours=8)))
    content = '\n'.join(content)
    print(content)
    utils.send_notification(content, args.token, args.topic_ids, args.uids)


if __name__ == '__main__':
    main()
