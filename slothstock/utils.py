#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for Slothstock.

File: utils.py
Author: huxuan
Email: i(at)huxuan.org
"""
from datetime import datetime
from datetime import timedelta

from wxpusher import WxPusher


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


def send_notification(stocks, title, token, topic_ids, uids):
    """Send buy signal notification."""
    if not token:
        return
    if not uids and not topic_ids:
        return
    content = [title]
    content.extend([
        f'{symbol} {stocks.loc[symbol, "name"]}'
        for symbol in stocks.index
    ])
    content.append(str(datetime.utcnow() + timedelta(hours=8)))
    WxPusher.send_message('\n'.join(content),
                          uids=uids,
                          topic_ids=topic_ids,
                          token=token)
