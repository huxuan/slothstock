#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for MACD.

File: test_macd_indicator.py
Author: huxuan
Email: i(at)huxuan.org
"""
from datetime import datetime
import unittest

from slothstock.indicators import macd_indicator
from slothstock.providers.xueqiu import XueQiu


class TestMACD(unittest.TestCase):
    """Unittests for MACD."""

    def test_is_about_to_top_divergence(self):
        """Positive case for top divergence."""
        res = XueQiu.kline('000016.SH', 'day', datetime(2019, 10, 21))
        macd, macdsignal, macdhist = macd_indicator.clean_macd(res.close)
        self.assertTrue(macd_indicator.is_positive(macd, macdsignal))
        self.assertTrue(macd_indicator.is_about_to_top_divergence(
            macd, macdsignal, macdhist))

    def test_is_about_to_bottom_divergence(self):
        """Positive case for bottom divergence."""
        res = XueQiu.kline('000016.SH', 'week', datetime(2019, 1, 11))
        macd, macdsignal, macdhist = macd_indicator.clean_macd(res.close)
        self.assertTrue(macd_indicator.is_negative(macd, macdsignal))
        self.assertTrue(macd_indicator.is_about_to_bottom_divergence(
            macd, macdsignal, macdhist))

    def test_is_expand_golden_cross(self):
        """Positive case for expand golden cross."""
        res = XueQiu.kline('000001.SH', 'day', '2020-01-03 00:00')
        _, _, macdhist = macd_indicator.clean_macd(res.close)
        self.assertTrue(macd_indicator.is_expand_golden_cross(macdhist))
