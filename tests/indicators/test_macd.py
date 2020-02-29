#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for MACD.

File: test_macd.py
Author: huxuan
Email: i(at)huxuan.org
"""
from datetime import datetime
import unittest

from slothstock.indicators import MACD
from slothstock.providers import XueQiu


class TestMACD(unittest.TestCase):
    """Unittests for MACD."""

    def test_death(self):
        """Test for death."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 1, 16))
        macd = MACD(res.close)
        self.assertTrue(macd.death)
        macd = MACD(res.close[:-1])
        self.assertFalse(macd.death)

    def test_golden(self):
        """Test for golden."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 17))
        macd = MACD(res.close)
        self.assertTrue(macd.golden)
        macd = MACD(res.close[:-1])
        self.assertFalse(macd.golden)

    def test_negative_positive_when_death(self):
        """Test for negative and positive when death cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 3))
        macd = MACD(res.close)
        self.assertTrue(macd.negative)
        self.assertFalse(macd.positive)
        macd = MACD(res.close[:-1])
        self.assertFalse(macd.negative)
        self.assertTrue(macd.positive)

    def test_negative_positive_when_golden(self):
        """Test for negative and positive when golden cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 24))
        macd = MACD(res.close)
        self.assertFalse(macd.negative)
        self.assertTrue(macd.positive)
        macd = MACD(res.close[:-1])
        self.assertTrue(macd.negative)
        self.assertFalse(macd.positive)

    def test_narrow_expand_when_narrow_in_golden(self):
        """Test for narrow and expand when just narrow in golden cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 25))
        macd = MACD(res.close)
        self.assertTrue(macd.narrow)
        self.assertFalse(macd.expand)
        macd = MACD(res.close[:-1])
        self.assertFalse(macd.narrow)
        self.assertTrue(macd.expand)

    def test_narrow_expand_when_narrow_in_death(self):
        """Test for narrow and expand when just narrow in death cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 6))
        macd = MACD(res.close)
        self.assertTrue(macd.narrow)
        self.assertFalse(macd.expand)
        macd = MACD(res.close[:-1])
        self.assertFalse(macd.narrow)
        self.assertTrue(macd.expand)

    def test_narrow_expand_when_cross_in_golden(self):
        """Test for narrow and expand when just cross in golden cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 2, 17))
        macd = MACD(res.close)
        self.assertFalse(macd.narrow)
        self.assertTrue(macd.expand)
        macd = MACD(res.close[:-1])
        self.assertTrue(macd.narrow)
        self.assertFalse(macd.expand)

    def test_narrow_expand_when_cross_in_death(self):
        """Test for narrow and expand when just cross in death cross."""
        res = XueQiu.kline('000001.SH', 'day', datetime(2020, 1, 16))
        macd = MACD(res.close)
        self.assertFalse(macd.narrow)
        self.assertTrue(macd.expand)
        macd = MACD(res.close[:-1])
        self.assertTrue(macd.narrow)
        self.assertFalse(macd.expand)

    def test_will_top_divergence(self):
        """Test for will_top_divergence property."""
        res = XueQiu.kline('000016.SH', 'day', datetime(2019, 10, 21))
        macd = MACD(res.close)
        self.assertTrue(macd.will_top_divergence)

    def test_will_bottom_divergence(self):
        """Test for will_bottom_divergence property."""
        res = XueQiu.kline('000016.SH', 'week', datetime(2019, 1, 11))
        macd = MACD(res.close)
        self.assertTrue(macd.will_bottom_divergence)
