#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom exceptions.

File: exceptions.py
Author: huxuan
Email: i(at)huxuan.org
"""


class BaseCustomException(RuntimeError):
    """Base Custom Exception."""


class InvalidDatetimeError(BaseCustomException):
    """Raised for invalid datetime."""


class InvalidResultError(BaseCustomException):
    """Raised when the result can not be parsed."""


class NoResponseError(BaseCustomException):
    """Raised when no response fetched."""


class NoResultError(BaseCustomException):
    """Raised when no result fetched."""


class XueQiuError(BaseCustomException):
    """Raised for specific error from XueQiu."""

    def __init__(self, code, message):
        """Init for XueQiuError."""
        super(XueQiuError, self).__init__()
        self.code = code
        self.message = message

    def __str__(self):
        """Str for XueQiuError."""
        return f'[{self.code}] {self.message}'
