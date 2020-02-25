#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collection of parsers.

File: parsers.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse

from slothstock import __version__

# MISC
MISC_PARSER = argparse.ArgumentParser(add_help=False)
MISC_GROUP = MISC_PARSER.add_argument_group('misc')
MISC_GROUP.add_argument('-d', '--daemon', action='store_true')
MISC_GROUP.add_argument('-i', '--interval', default=0.1, type=float)
MISC_GROUP.add_argument('-o', '--output', default='sloth.ebk')
MISC_GROUP.add_argument('-v', '--version', action='version',
                        version=__version__)

# SlothStock
SLOTHSTOCK_PARSER = argparse.ArgumentParser(add_help=False)
SLOTHSTOCK_GROUP = SLOTHSTOCK_PARSER.add_argument_group('slothstock')
SLOTHSTOCK_GROUP.add_argument('--reserve-st', action='store_true')
SLOTHSTOCK_GROUP.add_argument('--reserve-suspend', action='store_true')
SLOTHSTOCK_GROUP.add_argument('-c', '--child-period', action='store_true')
SLOTHSTOCK_GROUP.add_argument('-e', '--ebk', action='append', default=[])
SLOTHSTOCK_GROUP.add_argument('-g', '--great-great-grandparent-period',
                              action='store_true')
SLOTHSTOCK_GROUP.add_argument('-p', '--period', default='day')
SLOTHSTOCK_GROUP.add_argument('-s', '--strict', action='store_true')

# WxPusher
WXPUSHER_PARSER = argparse.ArgumentParser(add_help=False)
WXPUSHER_GROUP = WXPUSHER_PARSER.add_argument_group('wxpusher')
WXPUSHER_GROUP.add_argument('--token')
WXPUSHER_GROUP.add_argument('--topic-ids', action="append", default=[])
WXPUSHER_GROUP.add_argument('--uids', action='append', default=[])
WXPUSHER_GROUP.add_argument('-t', '--title')
