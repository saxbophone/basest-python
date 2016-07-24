#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def ints_to_symbols(ints, symbol_table):
    """
    Given an iterable of ints and a list of symbols to convert them to, convert
    them to an iterable of symbols and return this.
    """
    return [symbol_table[i] for i in ints]


def symbols_to_ints(symbols, symbol_table):
    """
    Given an iterable of symbols a list of symbols to convert them from,
    convert them to an iterable of ints and return this.
    """
    return [symbol_table.index(s) for s in symbols]
