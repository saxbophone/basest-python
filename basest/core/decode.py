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

from ..exceptions import InvalidInputLengthError
from .encode import encode_raw
from .utils import ints_to_symbols, symbols_to_ints, validate_symbol_tables


def decode_raw(input_base, output_base, input_ratio, output_ratio, input_data):
    """
    Given an input base, an output base, input ratio, output ratio and input
    data (as an iterable of integers), return an iterable of integers of the
    input data decoded into the output base, using the given ratios. Interprets
    the integer that is 1 more than the input base's max integer as a padding
    symbol (so interpretted padding integer for decoding base64 would be 64, as
    base64 input would be in the range 0-63).
    """
    # raise an exception early if padding was truncated
    if len(input_data) % input_ratio != 0:
        raise InvalidInputLengthError(
            'Decoding requires input length to be an exact multiple of the '
            'input ratio, or for padding to be used to ensure this.'
        )
    # create a 'workon' copy of the input data so we don't end up changing it
    input_workon = list(input_data)
    # count number of padding symbols
    padding_length = input_workon.count(input_base)
    # now, replace all padding symbols with the maximmum symbol
    '''
    Explanation: This solution is for bases that don't match up exactly, given
    their chosen ratios. It was inspired by the same technique that is used in
    base85/ascii85 decoding and does not negatively impact 'perfect' aligning
    bases such as base64.
    '''
    input_workon = [
        (s if s != input_base else input_base - 1) for s in input_workon
    ]
    # use the encode_raw function to convert the data
    output_data = encode_raw(
        input_base=input_base, output_base=output_base,
        input_ratio=input_ratio, output_ratio=output_ratio,
        input_data=input_workon
    )
    # strip off the unnecessary padding symbols if there was padding
    [output_data.pop() for _ in range(padding_length)]
    return output_data


def decode(
    input_base, input_symbol_table, input_padding,
    output_base, output_symbol_table,
    input_ratio, output_ratio, input_data
):
    """
    Given input and output bases, ratios, symbol tables, the padding symbol
    used by the input data and the input data to denode, return an iterable
    of the data decoded from the input base to the output base.
    Assumes standard base64-style padding using the given input padding symbol,
    but can handle unpadded input just fine.
    """
    # validate both symbol tables and the padding symbol before continuing
    validate_symbol_tables(
        input_symbol_table,
        input_padding,
        output_symbol_table
    )
    # create workon copy of input data and convert symbols to raw ints
    # NOTE: input symbol table here includes the padding character
    input_workon = symbols_to_ints(
        input_data, input_symbol_table + [input_padding]
    )
    # use decode_raw() to decode the data
    output_data = decode_raw(
        input_base=input_base, output_base=output_base,
        input_ratio=input_ratio, output_ratio=output_ratio,
        input_data=input_workon
    )
    # convert raw output data back to symbols using output symbol table
    return ints_to_symbols(output_data, output_symbol_table)
