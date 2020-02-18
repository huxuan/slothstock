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
from slothstock.providers.xueqiu import XueQiu


class TestUtils(unittest.TestCase):
    """Unittests for utils."""

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
