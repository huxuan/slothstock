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


def clean_macd(closes, fastperiod=12, slowperiod=26, signalperiod=9):
    """Calculate MACD with clean up."""
    macd, macdsignal, macdhist = talib.MACD(
        closes, fastperiod, slowperiod, signalperiod)
    macd = macd[~numpy.isnan(macd)]
    macdsignal = macdsignal[~numpy.isnan(macdsignal)]
    macdhist = macdhist[~numpy.isnan(macdhist)]
    return macd, macdsignal, macdhist


def is_expand_golden_cross(macdhist):
    """Check whether the macd is expanding golden cross."""
    if len(macdhist) < 2:
        return False
    return macdhist[-1] >= 0 and macdhist[-1] >= macdhist[-2]


def is_negative(macd, macdsignal, strict=True):
    """Check whether the macd is negative."""
    if len(macd) < 1:
        return False
    if strict:
        return macd[-1] <= 0 and macdsignal[-1] <= 0
    return macd[-1] <= 0 or macdsignal[-1] <= 0


def is_positive(macd, macdsignal, strict=True):
    """Check whether the macd is positive."""
    if len(macd) < 1:
        return False
    if strict:
        return macd[-1] >= 0 and macdsignal[-1] >= 0
    return macd[-1] >= 0 or macdsignal[-1] >= 0


def is_about_to_death_cross(macdhist, strict=True):
    """Check whether is going to be death cross."""
    if len(macdhist) < 1 or macdhist[-1] < 0:
        return False
    if strict:
        return len(macdhist) > 1 and macdhist[-2] >= macdhist[-1]
    return True


def is_about_to_golden_cross(macdhist, strict=True):
    """Check whether is going to be golden cross."""
    if len(macdhist) < 1 or macdhist[-1] > 0:
        return False
    if strict:
        return len(macdhist) > 1 and macdhist[-2] <= macdhist[-1]
    return True


def is_about_to_top_divergence(macd, macdsignal, macdhist, strict=True):
    """Check whether is going to be top divergence."""
    if not is_about_to_death_cross(macdhist, strict):
        return False

    idx_negative = numpy.where(macdhist <= 0)[0]
    if len(idx_negative) < 1:
        return False
    idx_golden_cross = idx_negative[-1]

    idx_positive = numpy.where(macdhist[:idx_golden_cross] >= 0)[0]
    if len(idx_positive) < 1:
        return False
    idx_death_cross = idx_positive[-1]

    if strict and any(macd[idx_death_cross:] < 0):
        return False
    if any(macdsignal[idx_death_cross:] < 0):
        return False
    return macdsignal[idx_death_cross] >= macdsignal[-1]


def is_about_to_bottom_divergence(macd, macdsignal, macdhist, strict=True):
    """Check whether is going to be bottom divergence."""
    if not is_about_to_golden_cross(macdhist, strict):
        return False

    idx_positive = numpy.where(macdhist >= 0)[0]
    if len(idx_positive) < 1:
        return False
    idx_death_cross = idx_positive[-1]

    idx_negative = numpy.where(macdhist[:idx_death_cross] <= 0)[0]
    if len(idx_negative) < 1:
        return False
    idx_golden_cross = idx_negative[-1]

    if strict and any(macd[idx_golden_cross:] > 0):
        return False
    if any(macdsignal[idx_golden_cross:] > 0):
        return False
    return macdsignal[idx_golden_cross] <= macdsignal[-1]
