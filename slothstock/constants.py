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
PERIODS_VALID = PERIODS[1:5]
STOCK_PREFIX_MARKET = {
    '00': 'SZ',
    '15': 'SZ',
    '30': 'SZ',
    '51': 'SH',
    '60': 'SH',
    '68': 'SH',
}
