#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parsers for scripts.

File: parsers.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse
from datetime import datetime

from slothstock import __version__
from slothstock.constants import CHILD_CHOICES
from slothstock.scripts import helps


# Buy only
BUY_PARSER = argparse.ArgumentParser(add_help=False)
_BUY_GROUP = BUY_PARSER.add_argument_group('Buy')
_BUY_GROUP.add_argument('--reserve-st', action='store_true',
                        help=helps.RESERVE_ST)
_BUY_GROUP.add_argument('--reserve-suspend', action='store_true',
                        help=helps.RESERVE_SUSPEND)
_BUY_GROUP.add_argument('--check-great-great-grandparent', action='store_true',
                        help=helps.CHECK_GREAT_GREAT_GRANDPARENT)

# MISC
MISC_PARSER = argparse.ArgumentParser(add_help=False)
MISC_PARSER.add_argument('--daemon', action='store_true', help=helps.DAEMON)
MISC_PARSER.add_argument('--interval', default=0.1, type=float,
                         help=helps.INTERVAL)
MISC_PARSER.add_argument('--ignore-empty', action='store_true',
                         help=helps.IGNORE_EMPTY)
MISC_PARSER.add_argument('--output', help=helps.OUTPUT)
MISC_PARSER.add_argument('-V', '--version', action='version',
                         version=__version__)

# Sell only
SELL_PARSER = argparse.ArgumentParser(add_help=False)
_SELL_GROUP = SELL_PARSER.add_argument_group('Sell')
_SELL_GROUP.add_argument('--check-parent', action='store_true',
                         help=helps.CHECK_PARENT)

# SlothStock
SLOTHSTOCK_PARSER = argparse.ArgumentParser(add_help=False)
_SLOTHSTOCK_GROUP = SLOTHSTOCK_PARSER.add_argument_group('SlothStock')
_SLOTHSTOCK_GROUP.add_argument('--ebk', action='append', default=[],
                               help=helps.EBK)
_SLOTHSTOCK_GROUP.add_argument('--period', default='day', help=helps.PERIOD)
_SLOTHSTOCK_GROUP.add_argument('--loose', action='store_true',
                               help=helps.LOOSE)
_SLOTHSTOCK_GROUP.add_argument('--child', choices=CHILD_CHOICES,
                               help=helps.CHILD)
_SLOTHSTOCK_GROUP.add_argument('--datetime', type=datetime.fromisoformat,
                               help=helps.DATETIME)

# WxPusher
WXPUSHER_PARSER = argparse.ArgumentParser(add_help=False)
_WXPUSHER_GROUP = WXPUSHER_PARSER.add_argument_group('WxPusher')
_WXPUSHER_GROUP.add_argument('--title', help=helps.TITLE)
_WXPUSHER_GROUP.add_argument('--token', help=helps.TOKEN)
_WXPUSHER_GROUP.add_argument('--topic-ids', action="append", default=[],
                             help=helps.TOPIC_IDS)
_WXPUSHER_GROUP.add_argument('--uids', action='append', default=[],
                             help=helps.UIDS)
