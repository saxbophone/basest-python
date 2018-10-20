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


def symbol_table_is_unique(symbol_table, padding_symbol=None):
    """
    Returns True if the given symbol table and padding symbol are unique,
    otherwise returns False.
    """
    # simple way of checking if a list of hashables is unique
    if len(symbol_table) != len(set(symbol_table)):
        return False
    else:
        # otherwise, check that padding_symbol isn't in the symbol table
        # NOTE: this assumes that `None` is never in the symbol table
        return padding_symbol not in symbol_table
