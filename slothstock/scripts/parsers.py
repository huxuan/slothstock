#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parsers for scripts.

File: parsers.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse

from slothstock import __version__

# Buy only
BUY_PARSER = argparse.ArgumentParser(add_help=False)
_BUY_GROUP = BUY_PARSER.add_argument_group('Buy')
_BUY_GROUP.add_argument('--reserve-st', action='store_true')
_BUY_GROUP.add_argument('--reserve-suspend', action='store_true')
_BUY_GROUP.add_argument('--check-great-great-grandparent', action='store_true')

# MISC
MISC_PARSER = argparse.ArgumentParser(add_help=False)
MISC_PARSER.add_argument('--daemon', action='store_true')
MISC_PARSER.add_argument('--interval', default=0.1, type=float)
MISC_PARSER.add_argument('--ignore-empty', action='store_true')
MISC_PARSER.add_argument('--output')
MISC_PARSER.add_argument('-V', '--version', action='version',
                         version=__version__)

# SlothStock
SLOTHSTOCK_PARSER = argparse.ArgumentParser(add_help=False)
_SLOTHSTOCK_GROUP = SLOTHSTOCK_PARSER.add_argument_group('SlothStock')
_SLOTHSTOCK_GROUP.add_argument('--ebk', action='append', default=[])
_SLOTHSTOCK_GROUP.add_argument('--period', default='day')
_SLOTHSTOCK_GROUP.add_argument('--loose', action='store_true')
_SLOTHSTOCK_GROUP.add_argument('--skip-child', action='store_true')

# WxPusher
WXPUSHER_PARSER = argparse.ArgumentParser(add_help=False)
_WXPUSHER_GROUP = WXPUSHER_PARSER.add_argument_group('WxPusher')
_WXPUSHER_GROUP.add_argument('--title')
_WXPUSHER_GROUP.add_argument('--token')
_WXPUSHER_GROUP.add_argument('--topic-ids', action="append", default=[])
_WXPUSHER_GROUP.add_argument('--uids', action='append', default=[])
