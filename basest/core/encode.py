#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def raw_encode(input_base, output_base, input_ratio, output_ratio, input_data):
    """
    Given an input base, an output base, input ratio, output ratio and input
    data (as an iterable of integers), return an iterable of integers of the
    input data encoded into the output base, using the given ratios. Uses the
    integer that is 1 more than the output base's max integer as a padding
    symbol (so padding integer for base64 encoding would be 64, as base64
    output would be in the range 0-63).
    """
    # create a 'workon' copy of the input data so we don't end up changing it
    before = list(input_data)
    # store length of input data for future reference
    input_length = len(before)
    # calculate the amount of overlap (if any)
    overlap = input_length % input_ratio
    '''
    get the nearest data length from the input data that is divisible by
    the input ratio, using overlap if there is any
    '''
    input_nearest_length = (
        input_length if overlap == 0
        else (
            (
                (
                    (input_length - overlap) // input_ratio
                ) + 1
            ) * input_ratio
        )
    )
    # calculate the amount of padding needed
    padding_length = (input_nearest_length - input_length)
    # get the output length, based on nearest divisible input length
    output_length = (input_nearest_length // input_ratio) * output_ratio
    # create a new list for the output data
    output_data = [0] * output_length
    # extend the input_data to the nearest divisible length (for padding)
    before.extend([0] * padding_length)
    # encode the data - store each group of input_ratio symbols in a number
    for i in range(0, input_nearest_length, input_ratio):
        store = 0
        for j in range(0, input_ratio):
            # store value of symbol
            symbol = before[i + j]
            # upscale it if neccessary, in a little-endian manner
            symbol *= (input_base ** (input_ratio - j - 1))
            # add to store
            store += symbol
        '''
        now that store contains the value of a number of symbols, separate this
        out to the output symbols
        '''
        for j in range(0, output_ratio):
            # convert output array index
            index = ((i // input_ratio) * output_ratio) + j
            # re-interpret the number in terms of output base
            symbol = store // (output_base ** (output_ratio - j - 1))
            # store at the calculated position
            output_data[index] = symbol
            # decrement the store variable, having now encoded part of it
            store -= (symbol * (output_base ** (output_ratio - j - 1)))
    # set padding bytes to padding symbol, if needed
    for i in range(output_length - padding_length, output_length):
        output_data[i] = output_base
    return output_data


def encode(
    input_base, input_symbol_table, output_base, output_symbol_table,
    output_padding, input_ratio, output_ratio, input_data
):
    """
    Given input and output bases, ratios, symbol tables, the padding symbol
    to use for output padding and the input data to encode, return an iterable
    of the data encoded from the input base to the output base.
    Uses standard base64-style padding if needed, using the given padding
    symbol.
    """
    # create workon copy of input data and convert symbols to raw ints
    before = [input_symbol_table.index(symbol) for symbol in input_data]
    # use raw_encode() to encode the data
    output_data = raw_encode(
        input_base=input_base, output_base=output_base,
        input_ratio=input_ratio, output_ratio=output_ratio, input_data=before
    )
    # assemble output symbol table using given table + padding symbol
    output_conversion = output_symbol_table + [output_padding]
    # convert raw output data back to symbols using output symbol table
    return [output_conversion[symbol] for symbol in output_data]
