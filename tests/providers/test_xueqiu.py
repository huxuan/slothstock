#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for XueQiu.

File: test_xueqiu.py
Author: huxuan
Email: i(at)huxuan.org
"""
import random
import unittest

import pandas

from slothstock.providers import XueQiu


class TestXueQiu(unittest.TestCase):
    """Unittests for XueQiu."""

    def test_kline(self):
        """Positive case for kline."""
        stocks = XueQiu.list_ashare(page=random.randint(1, 1000), size=1)
        res = XueQiu.kline(stocks.index[0])
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertGreater(len(res.index), 0)

    def test_list(self):
        """Positive case for list."""
        res = XueQiu.list()
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertGreater(len(res.index), 0)

    def test_list_ashare(self):
        """Positive case for list_ashare."""
        res = XueQiu.list_ashare()
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertGreater(len(res.index), 0)

    def test_list_etf(self):
        """Positive case for list_etf."""
        res = XueQiu.list_etf()
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertGreater(len(res.index), 0)

    def test_list_index(self):
        """Positive case for list_index."""
        res = XueQiu.list_index()
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertEqual(len(res.index), 4)
