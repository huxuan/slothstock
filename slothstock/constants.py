#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom constants.

File: constants.py
Author: huxuan
Email: i(at)huxuan.org
"""

DATETIME_FORMAT = '%Y-%m-%d %H:%M'
FORMAT_EBK = 'ebk'
HEADER_USER_AGENT = 'User-Agent'
PERIODS = [
    '1m',
    '5m',
    '15m',
    '60m',
    'day',
    'week',
    'month',
    'quarter',
    'year',
]
STOCK_INDEX = {
    '000001.SH',
    '000300.SH',
    '399001.SZ',
    '399006.SZ',
}
STOCK_PREFIX_MARKET = {
    '00': 'SZ',
    '15': 'SZ',
    '30': 'SZ',
    '51': 'SH',
    '60': 'SH',
    '68': 'SH',
}
CHILD_CHOICE_CROSS = 'cross'
CHILD_CHOICE_DIVERGENCE = 'divergence'
CHILD_CHOICES = [
    CHILD_CHOICE_CROSS,
    CHILD_CHOICE_DIVERGENCE,
]
KLINE_COLUMNS = [
    'amount',
    'chg',
    'close',
    'high',
    'low',
    'open',
    'percent',
    'timestamp',
    'turnoverrate',
    'volume',
]
LIST_COLUMNS = [
    'amount',
    'amplitude',
    'chg',
    'current',
    'current_year_percent',
    'dividend_yield',
    'float_market_capital',
    'float_shares',
    'issue_date_ts',
    'main_net_inflows',
    'market_capital',
    'name',
    'pb',
    'pb_ttm',
    'pe_ttm',
    'percent',
    'rating',
    'turnover_rate',
    'type',
    'volume',
    'volume_ratio',
]
