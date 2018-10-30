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

from ..exceptions import ImproperUsageError
from .utils import ints_to_symbols, symbols_to_ints, validate_symbol_tables


def _nearest_length(input_length, input_ratio):
    """
    Returns the nearest data length from the input data that is divisible by
    the input ratio, using overlap if there is any.
    """
    # calculate the amount of overlap (if any)
    overlap = input_length % input_ratio
    # calculate the nearest input length that can contain our length
    return (
        input_length if overlap == 0
        else ((((input_length - overlap) // input_ratio) + 1) * input_ratio)
    )


def encode_raw(input_base, output_base, input_ratio, output_ratio, input_data):
    """
    Given an input base, an output base, input ratio, output ratio and input
    data (as an iterable of integers), return an iterable of integers of the
    input data encoded into the output base, using the given ratios. Uses the
    integer that is 1 more than the output base's max integer as a padding
    symbol (so padding integer for base64 encoding would be 64, as base64
    output would be in the range 0-63).
    """
    # create a 'workon' copy of the input data so we don't end up changing it
    input_workon = list(input_data)
    # store length of input data for future reference
    input_length = len(input_workon)
    '''
    Special validation: if the output base is larger than the input base, then
    the length of the input data MUST be an exact multiple of the input ratio.
    Otherwise, the data will be corrupted if we continue, so we will raise
    ImproperUsageError instead.
    '''
    if input_base < output_base and input_length % input_ratio != 0:
        raise ImproperUsageError(
            'Input data length must be exact multiple of input ratio when '
            'output base is larger than input base'
        )
    # get nearest data length that the input data fits in
    input_nearest_length = _nearest_length(input_length, input_ratio)
    # calculate the amount of padding needed
    padding_length = (input_nearest_length - input_length)
    # get the output length, based on nearest divisible input length
    output_length = (input_nearest_length // input_ratio) * output_ratio
    # create a new list for the output data
    output_data = [0] * output_length
    # extend the input_data to the nearest divisible length (for padding)
    input_workon.extend([0] * padding_length)
    # encode the data - store each group of input_ratio symbols in a number
    for i in range(0, input_nearest_length, input_ratio):
        store = 0
        for j in range(0, input_ratio):
            # store value of symbol
            symbol = input_workon[i + j]
            # upscale it if neccessary, in a little-endian manner
            symbol *= (input_base ** (input_ratio - j - 1))
            # add to store
            store += symbol
        '''
        now that store contains the value of a number of symbols, separate this
        out to the output symbols
        '''
        for k in range(0, output_ratio):
            # convert output array index
            index = ((i // input_ratio) * output_ratio) + k
            # re-interpret the number in terms of output base
            symbol = store // (output_base ** (output_ratio - k - 1))
            # store at the calculated position
            output_data[index] = symbol
            # decrement the store variable, having now encoded part of it
            store -= (symbol * (output_base ** (output_ratio - k - 1)))
    # set padding bytes to padding symbol, if needed
    for i in range(output_length - padding_length, output_length):
        output_data[i] = output_base
    return output_data


def encode(
    input_base, input_symbol_table,
    output_base, output_symbol_table, output_padding,
    input_ratio, output_ratio, input_data
):
    """
    Given input and output bases, ratios, symbol tables, the padding symbol
    to use for output padding and the input data to encode, return an iterable
    of the data encoded from the input base to the output base.
    Uses standard base64-style padding if needed, using the given padding
    symbol.
    """
    # validate both symbol tables and the padding symbol before continuing
    validate_symbol_tables(
        output_symbol_table,
        output_padding,
        input_symbol_table
    )
    # create workon copy of input data and convert symbols to raw ints
    input_workon = symbols_to_ints(input_data, input_symbol_table)
    # use encode_raw() to encode the data
    output_data = encode_raw(
        input_base=input_base, output_base=output_base,
        input_ratio=input_ratio, output_ratio=output_ratio,
        input_data=input_workon
    )
    # convert raw output data back to symbols using output symbol table
    # NOTE: output symbol table here includes the padding character
    return ints_to_symbols(output_data, output_symbol_table + [output_padding])
