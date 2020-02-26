#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for utils.

File: test_utils.py
Author: huxuan
Email: i(at)huxuan.org
"""
import random
import tempfile
import unittest

from slothstock import utils
from slothstock.providers import XueQiu


class TestUtils(unittest.TestCase):
    """Unittests for utils."""

    @classmethod
    def setUpClass(cls):
        """Set up for class."""
        cls.stocks = XueQiu.list_stocks()

    def test_import_export_ebk(self):
        """Positive case for import & export ebk."""
        temp_file = tempfile.NamedTemporaryFile()
        stocks = XueQiu.list_ashare(
            page=random.randint(1, 20),
            size=random.randint(1, 100))
        utils.export_ebk(stocks.index, temp_file.name)
        symbols = utils.import_ebk(temp_file.name)
        for symbol in symbols:
            self.assertIn(symbol, stocks.index)

    def test_is_st(self):
        """Cases to check whether is ST."""
        self.assertTrue(utils.is_st(self.stocks.loc['600518.SH']))
        self.assertFalse(utils.is_st(self.stocks.loc['000001.SZ']))

    def test_is_suspend(self):
        """Cases to check whether is suspended."""
        self.assertTrue(utils.is_suspend(self.stocks.loc['000029.SZ']))
        self.assertTrue(utils.is_suspend(self.stocks.loc['002450.SZ']))
        self.assertTrue(utils.is_suspend(self.stocks.loc['300104.SZ']))
        self.assertTrue(utils.is_suspend(self.stocks.loc['600145.SH']))

        self.assertFalse(utils.is_suspend(self.stocks.loc['000001.SH']))
        self.assertFalse(utils.is_suspend(self.stocks.loc['510050.SH']))
        self.assertFalse(utils.is_suspend(self.stocks.loc['600519.SH']))

        self.assertFalse(utils.is_suspend(self.stocks.loc['000001.SZ']))
        self.assertFalse(utils.is_suspend(self.stocks.loc['159949.SZ']))
        self.assertFalse(utils.is_suspend(self.stocks.loc['399001.SZ']))
