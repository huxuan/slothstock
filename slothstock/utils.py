#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for Slothstock.

File: utils.py
Author: huxuan
Email: i(at)huxuan.org
"""

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


def send_notification(content, token, topic_ids, uids):
    """Send notification."""
    if not token:
        return
    if not uids and not topic_ids:
        return
    WxPusher.send_message(content, uids=uids, topic_ids=topic_ids, token=token)
