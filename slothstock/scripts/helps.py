#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Help messages for scripts.

File: help.py
Author: huxuan
Email: i(at)huxuan.org
"""
from slothstock.constants import CHILD_CHOICES
from slothstock.constants import PERIODS

CHECK_GREAT_GREAT_GRANDPARENT = 'Flag to check great_great_grandparent period.'
CHECK_PARENT = 'Flag to check parent period.'
CHILD = 'Child check mode, it should be `%s`. If no specified, child ' \
    'period check will be skipped.' % '` or `'.join(CHILD_CHOICES)
DAEMON = 'Flag of daemon mode, no console output.'
DATETIME = 'The datetime compatible with ISO 8601 format (`YY-MM-DD` or ' \
    '`YYYY-MM-DDTHH:MM`) for signal check, mostly for testing purpose.'
EBK = 'Stock candidates in ebk format file. If not specified, all stocks ' \
    'are processed. Note that multiple of them are supported.'
IGNORE_EMPTY = 'Flag for no output or notification when the result is empty.'
INTERVAL = 'Time interval in seconds between successive requests in providers.'
LOOSE = 'Flag of loose mode for signal check.'
OUTPUT = 'The output file in ebk format for the results.'
PERIOD = 'Check signal for specific period. Valid choices are `%s`.' % \
    '`, `'.join(PERIODS)
RESERVE_ST = 'Flag to reserve ST stocks.'
RESERVE_SUSPEND = 'Flag to reserve suspended stocks.'
TITLE = 'The `title` for the notification.'
TOKEN = 'The `token` for the notification. None means no notification'
TOPIC_IDS = 'The `topic_ids` for the notification. Note that multiple of ' \
    'them are supported and no notification will be sent if both ' \
    '`topic_ids` and `uids` are None, '
UIDS = 'The `uids` for the notification. Note that multiple of them are ' \
    'supported and no notification will be sent if both `topic_ids` and ' \
    '`uids` are None.'
