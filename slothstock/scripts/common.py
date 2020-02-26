#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common utilities for scripts.

File: common.py
Author: huxuan
Email: i(at)huxuan.org
"""
from datetime import datetime
from datetime import timedelta

from wxpusher import WxPusher

from slothstock import utils


def combine_content(title, stocks):
    """Combine title and stocks to message content."""
    content = [title]
    content.extend([
        f'{symbol} {stocks.loc[symbol, "name"]}'
        for symbol in stocks.index
    ])
    content.append(str(datetime.utcnow() + timedelta(hours=8)))
    return '\n'.join(content)


def show_result(stocks, action, args):
    """Show results."""
    # Return for empty result when set to ignore empty.
    if args.ignore_empty and stocks.index.empty:
        return

    # Output a file when output is set.
    if args.output:
        utils.export_ebk(stocks.index, args.output)

    # Send notification if token and (uids or topic_ids) is set.
    if args.token and (args.uids or args.topic_ids):
        # Format title.
        title = args.title
        if not title:
            if stocks.index.empty:
                title = f'{args.period}级别无可能{action}点'
            else:
                title = f'{args.period}级别可能{action}点'

        content = combine_content(title, stocks)
        WxPusher.send_message(content,
                              token=args.token,
                              uids=args.uids,
                              topic_ids=args.topic_ids)
