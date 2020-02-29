#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MACD indicator.

File: macd.py
Author: huxuan
Email: i(at)huxuan.org
"""
import numpy
import talib


class MACD():
    """MACD indicator."""

    def __init__(self, close):
        """Init for MACD."""
        self.diff, self.dea, self.macd = talib.MACD(close)
        self.diff = self.diff[~numpy.isnan(self.diff)]
        self.dea = self.dea[~numpy.isnan(self.dea)]
        self.macd = self.macd[~numpy.isnan(self.macd)]
        self.len = len(self.diff)

    @property
    def death(self):
        """Whether it is death cross."""
        return self.len and self.macd[-1] < 0

    @property
    def golden(self):
        """Whether it is golden cross."""
        return self.len and self.macd[-1] > 0

    @property
    def negative(self):
        """Whether it is negative."""
        return self.len and self.diff[-1] < 0

    @property
    def positive(self):
        """Whether it is positive."""
        return self.len and self.diff[-1] > 0

    @property
    def narrow(self):
        """Whether it is narrow."""
        return self.len > 1 and self.macd[-1] * self.macd[-2] > 0 and \
            abs(self.macd[-2]) >= abs(self.macd[-1])

    @property
    def expand(self):
        """Whether it is expand."""
        return self.len > 1 and (self.macd[-1] * self.macd[-2] < 0 or
                                 abs(self.macd[-2]) <= abs(self.macd[-1]))

    @property
    def will_top_divergence(self):
        """Whether it is going to be top divergence."""
        if not self.positive or not self.golden or not self.narrow:
            return False

        idx_negative = numpy.where(self.macd < 0)[0]
        if len(idx_negative) < 1:
            return False
        idx_golden = idx_negative[-1]

        idx_positive = numpy.where(self.macd[:idx_golden] > 0)[0]
        if len(idx_positive) < 1:
            return False
        idx_death = idx_positive[-1]

        return all(self.dea[idx_death:] > 0) and \
            self.dea[idx_death] >= self.dea[-1]

    @property
    def will_bottom_divergence(self):
        """Whether it is going to be bottom divergence."""
        if not self.negative and not self.death or not self.narrow:
            return False

        idx_positive = numpy.where(self.macd >= 0)[0]
        if len(idx_positive) < 1:
            return False
        idx_death = idx_positive[-1]

        idx_negative = numpy.where(self.macd[:idx_death] <= 0)[0]
        if len(idx_negative) < 1:
            return False
        idx_golden = idx_negative[-1]

        return all(self.dea[idx_golden:] < 0) and \
            self.dea[idx_golden] <= self.dea[-1]
