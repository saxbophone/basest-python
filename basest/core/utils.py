#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..exceptions import InvalidSymbolTableError


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


def _symbol_table_is_unique(symbol_table, padding_symbol=None):
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


def validate_symbol_tables(symbol_table, padding_symbol, other_symbol_table):
    """
    Validates two symbol tables (the padding symbol being used alongside the
    first one).
    Raises InvalidSymbolTableError if either of the symbol tables (or padding
    symbol) fail validation.
    """
    # first check that they all do not contain None
    if None in (symbol_table + [padding_symbol] + other_symbol_table):
        raise InvalidSymbolTableError(
            'None cannot be used in symbol tables nor for padding'
        )
    # if that check passes, validate tables (and padding) for uniqueness
    # the padding symbol is evaluated with the first symbol table
    elif (
        (not _symbol_table_is_unique(symbol_table, padding_symbol)) or
        (not _symbol_table_is_unique(other_symbol_table))
    ):
        raise InvalidSymbolTableError('Unique symbol tables required')
