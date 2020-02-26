#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for Slothstock.

File: utils.py
Author: huxuan
Email: i(at)huxuan.org
"""
from faker import Faker
import numpy
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from slothstock import constants


def export_ebk(symbols, filename='sloth.ebk'):
    """Export symbols in ebk format."""
    res = [b'']
    for symbol in symbols:
        code, exchange = symbol.split('.')
        if exchange == 'SH':
            res.append(f'1{code}'.encode())
        else:
            res.append(f'0{code}'.encode())

    with open(filename, 'wb') as fout:
        fout.write(b'\r\n'.join(res))


def import_ebk(filename):
    """Import symbols from ebk format."""
    res = []
    with open(filename, 'rb') as fin:
        fin.readline()  # The first line is useless.
        for line in fin:
            line = line.decode().strip()
            if line[0] == '1':
                res.append(f'{line[1:]}.SH')
            else:
                res.append(f'{line[1:]}.SZ')
    return res


def is_st(stock):
    """Check whether it is ST."""
    return 'ST' in stock.get('name')


def is_suspend(stock):
    """Check whether it is suspended."""
    return stock.get('type') == 11 and numpy.isnan(stock.get('amplitude'))


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
