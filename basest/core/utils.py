# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..exceptions import InvalidInputError, InvalidSymbolTableError


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

    Raises InvalidInputError if a symbol that is not in the symbol table is
    encountered.
    """
    try:
        return [symbol_table.index(s) for s in symbols]
    except ValueError:
        """
        This error is raised when index() doesn't find the given symbol in the
        symbol table. We're catching it because we want to raise our own
        exception class for this instead, InvalidInputError.
        """
        raise InvalidInputError('Encountered symbol not found in symbol table')


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
