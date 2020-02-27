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

from slothstock.indicators.macd_indicator import clean_macd
from slothstock.indicators.macd_indicator import is_about_to_bottom_divergence
from slothstock.indicators.macd_indicator import is_about_to_death_cross
from slothstock.indicators.macd_indicator import is_about_to_golden_cross
from slothstock.indicators.macd_indicator import is_about_to_top_divergence
from slothstock.indicators.macd_indicator import is_death_cross
from slothstock.indicators.macd_indicator import is_golden_cross
from slothstock.indicators.macd_indicator import is_negative
from slothstock.indicators.macd_indicator import is_positive
from slothstock.providers import XueQiu


class TestMACD(unittest.TestCase):
    """Unittests for MACD."""

    def test_is_about_to_top_divergence(self):
        """Positive case for top divergence."""
        res = XueQiu.kline('000016.SH', 'day', datetime(2019, 10, 21))
        macd, macdsignal, macdhist = clean_macd(res.close)
        self.assertTrue(is_about_to_top_divergence(
            macd, macdsignal, macdhist))

    def test_is_about_to_bottom_divergence(self):
        """Positive case for bottom divergence."""
        res = XueQiu.kline('000016.SH', 'week', datetime(2019, 1, 11))
        macd, macdsignal, macdhist = clean_macd(res.close)
        self.assertTrue(is_about_to_bottom_divergence(
            macd, macdsignal, macdhist))

    def test_is_negative(self):
        """Test is_negative() with loose."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 6))
        macd, macdsignal, _ = clean_macd(res.close)
        self.assertTrue(is_negative(macd, macdsignal))
        self.assertTrue(is_negative(macd, macdsignal, True))
        self.assertFalse(is_negative(macd[:-1], macdsignal[:-1]))
        self.assertTrue(is_negative(macd[:-1], macdsignal[:-1], True))

    def test_is_positive(self):
        """Test is_positive() with loose."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2019, 12, 18))
        macd, macdsignal, _ = clean_macd(res.close)
        self.assertTrue(is_positive(macd, macdsignal))
        self.assertTrue(is_positive(macd, macdsignal, True))
        self.assertFalse(is_positive(macd[:-1], macdsignal[:-1]))
        self.assertTrue(is_positive(macd[:-1], macdsignal[:-1], True))

    def test_is_death_cross(self):
        """Test is_death_cross() with loose."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 6))
        _, _, macdhist = clean_macd(res.close)
        self.assertFalse(is_death_cross(macdhist))
        self.assertTrue(is_death_cross(macdhist, True))
        self.assertTrue(is_death_cross(macdhist[:-1]))
        self.assertTrue(is_death_cross(macdhist[:-1], True))

    def test_is_golden_cross(self):
        """Test is_golden_cross() with loose."""
        res = XueQiu.kline('000001.SH', 'day', '2019-12-19 00:00')
        _, _, macdhist = clean_macd(res.close)
        self.assertFalse(is_golden_cross(macdhist))
        self.assertTrue(is_golden_cross(macdhist, True))
        self.assertTrue(is_golden_cross(macdhist[:-1]))
        self.assertTrue(is_golden_cross(macdhist[:-1], True))

    def test_is_about_death_cross(self):
        """Test is_about_to_death_cross() with loose."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2019, 12, 19))
        _, _, macdhist = clean_macd(res.close)
        self.assertTrue(is_about_to_death_cross(macdhist))
        self.assertTrue(is_about_to_death_cross(macdhist, True))
        self.assertFalse(is_about_to_death_cross(macdhist[:-1]))
        self.assertTrue(is_about_to_death_cross(macdhist[:-1], True))

    def test_is_about_golden_cross(self):
        """Test is_about_to_golden_cross() with loose."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 6))
        _, _, macdhist = clean_macd(res.close)
        self.assertTrue(is_about_to_golden_cross(macdhist))
        self.assertTrue(is_about_to_golden_cross(macdhist, True))
        self.assertFalse(is_about_to_golden_cross(macdhist[:-1]))
        self.assertTrue(is_about_to_golden_cross(macdhist[:-1], True))
