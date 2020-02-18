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

from faker import Faker
import pandas
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .. import constants
from .. import exceptions

XUEQIU_INDEX_URL = 'https://xueqiu.com/'
XUEQIU_KLINE_URL = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
XUEQIU_LIST_URL = 'https://xueqiu.com/service/v5/stock/screener/quote/list'
XUEQIU_ETF_LIST_URL = 'https://xueqiu.com/service/v5/stock/screener/fund/list'


def create_fake_session(index_url=None):
    """Create fake seesion."""
    session = requests.Session()
    session.headers[constants.HEADER_USER_AGENT] = Faker().internet_explorer()
    if index_url:  # Browser index page for cookies.
        requests_retry_session(session).get(index_url)
    return session


def requests_retry_session(
        session=None,
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)):
    """Send requests with retry."""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


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

    session = create_fake_session(XUEQIU_INDEX_URL)

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
        res = requests_retry_session(cls.session).get(
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
        res = requests_retry_session(cls.session).get(url, params=params)
        res = check_response(res)

        data = pandas.DataFrame(res['data']['list'])
        data.symbol = data.symbol.apply(symbol_restore)
        data.set_index('symbol', inplace=True)
        return data

    @classmethod
    def list_ashare(cls, **params):
        """List A Share stocks."""
        data = cls.list(**params)
        return data[data.index.str[:3].isin(constants.ASHARE_PREFIX)]

    @classmethod
    def list_etf(cls, **params):
        """List ETFs."""
        params.update({
            'parent_type': 1,
            'size': params.get('size', 300),
            'type': 18,
        })
        return cls.list(XUEQIU_ETF_LIST_URL, **params)


class XueQiu(metaclass=MetaXueQiu):  # pylint: disable=too-few-public-methods
    """XueQiu provider."""
