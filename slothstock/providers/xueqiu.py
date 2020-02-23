#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Xueqiu provider.

File: xueqiu.py
Author: huxuan
Email: i(at)huxuan.org
"""
from datetime import datetime
from datetime import timedelta

import pandas

from slothstock import constants
from slothstock import exceptions
from slothstock import utils

XUEQIU_ETF_LIST_URL = 'https://xueqiu.com/service/v5/stock/screener/fund/list'
XUEQIU_KLINE_URL = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
XUEQIU_LIST_URL = 'https://xueqiu.com/service/v5/stock/screener/quote/list'
XUEQIU_QUOTE_URL = 'https://xueqiu.com/service/v5/stock/batch/quote'
XUEQIU_URL = 'https://xueqiu.com/'


def symbol_transform(symbol):
    """Transform symbol for XueQiu."""
    return ''.join(symbol.split('.')[::-1])


def symbol_restore(symbol):
    """Restore symbol for XueQiu."""
    return f'{symbol[2:]}.{symbol[:2]}'


def datetime_to_timestamp(dt_origin=None):
    """Convert local datetime to utc timestamp."""
    if dt_origin is None:
        dt_origin = datetime.utcnow() + timedelta(hours=8)
    elif isinstance(dt_origin, str):
        dt_origin = datetime.strptime(dt_origin, constants.DATETIME_FORMAT)
    elif not isinstance(dt_origin, datetime):
        raise exceptions.InvalidDatetimeError(dt_origin)
    return int(dt_origin.timestamp() * 1000)


def timestamp_to_datetime(timestamp):
    """Convert utc timestamp to local datetime."""
    return datetime.fromtimestamp(timestamp / 1000)


def check_response(res):
    """Roughly check result in common."""
    if not res:
        raise exceptions.NoResponseError(res.status_code)

    try:
        res = res.json()
    except ValueError:
        return exceptions.InvalidResultError(res.content)

    if res.get('error_code') != 0:
        return exceptions.XueQiuError(
            res['error_code'],
            res['error_description'])

    if not res.get('data'):
        raise exceptions.NoResultError(res.content)

    return res


class MetaXueQiu(type):
    """Metaclass for XueQiu."""

    session = utils.create_fake_session(XUEQIU_URL)

    @classmethod
    def kline(cls, symbol, period='day', begin=None, count=142):
        """Fetch kline information."""
        params = {
            'begin': datetime_to_timestamp(begin),
            'count': -abs(count),
            'indicator': 'kline',
            'period': period,
            'symbol': symbol_transform(symbol),
            'type': 'before',
        }
        res = utils.requests_retry_session(cls.session).get(
            XUEQIU_KLINE_URL, params=params)
        res = check_response(res)

        data = pandas.DataFrame(
            data=res['data'].get('item'),
            columns=res['data'].get('column'))
        data.rename(columns={'timestamp': 'datetime'}, inplace=True)
        data.datetime = data.datetime.apply(timestamp_to_datetime)
        data.set_index('datetime', inplace=True)
        return data

    @classmethod
    def list(cls, url=XUEQIU_LIST_URL, **params):
        """List stock information."""
        params.update({
            '_': datetime_to_timestamp(),
            'order': params.get('reverse', False) and 'desc' or 'asc',
            'order_by': params.get('order_by', 'symbol'),
            'page': params.get('page', 1),
            'size': params.get('size', 4000),
            'type': params.get('type', 'sh_sz'),
        })
        res = utils.requests_retry_session(cls.session).get(url, params=params)
        res = check_response(res)

        data = pandas.DataFrame(res['data']['list'])
        data.symbol = data.symbol.apply(symbol_restore)
        data.set_index('symbol', inplace=True)
        return data

    @classmethod
    def list_ashare(cls, **params):
        """List A Share stocks."""
        data = cls.list(**params)
        return data[data.index.str[:2].isin(constants.STOCK_PREFIX_MARKET)]

    @classmethod
    def list_etf(cls, **params):
        """List ETF."""
        params.update({
            'parent_type': 1,
            'size': params.get('size', 300),
            'type': 18,
        })
        return cls.list(XUEQIU_ETF_LIST_URL, **params)

    @classmethod
    def list_index(cls, indexes=None):
        """List Index."""
        url = XUEQIU_QUOTE_URL
        indexes = indexes or [symbol_transform(index)
                              for index in constants.STOCK_INDEX]
        params = {
            '_': datetime_to_timestamp(),
            'symbol': ','.join(indexes or constants.STOCK_INDEX),
        }
        res = utils.requests_retry_session(cls.session).get(url, params=params)
        res = check_response(res)

        data = pandas.DataFrame([
            item['quote'] for item in res['data'].get('items', [])
        ])
        data.symbol = data.symbol.apply(symbol_restore)
        data.set_index('symbol', inplace=True)
        return data

    @classmethod
    def list_stocks(cls, ebk=None):
        """List stocks."""
        stocks_ashare = XueQiu.list_ashare()
        stocks_etf = XueQiu.list_etf()
        stocks_index = XueQiu.list_index()
        stocks = pandas.concat([stocks_ashare, stocks_etf, stocks_index])

        if ebk:
            res = set()
            for filename in ebk:
                res.update(utils.import_ebk(filename))
            stocks = stocks[stocks.index.isin(res)]

        return stocks


class XueQiu(metaclass=MetaXueQiu):  # pylint: disable=too-few-public-methods
    """XueQiu provider."""
