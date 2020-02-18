#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom constants.

File: constants.py
Author: huxuan
Email: i(at)huxuan.org
"""

ASHARE_PREFIX = set({
    '000',
    '001',
    '002',
    '003',
    '300',
    '600',
    '601',
    '603',
    '688',
})
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
