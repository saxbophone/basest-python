#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from math import ceil


def encode_stream_raw(
    input_base,
    output_base,
    input_ratio,
    output_ratio,
    input_data
):
    """
    Streaming encoder returning a generator which yields data of the input base
    from the input iterable, converted to the output base.
    """
    # these counters are for the input and output data 'chunks'
    input_index = 0
    # output_index = 0
    # this accumulator saturates for each input chunk and extracted to output
    accumulator = 0
    for input_symbol in input_data:
        # saturate the accumulator with this symbol, shifted for big-endianness
        accumulator += (
            input_symbol * input_base ** (input_ratio - input_index - 1)
        )
        input_index += 1
        input_index %= input_ratio
        # if we've finished processing one input chunk
        if input_index == 0:
            # serialise saturated accumulator to output base
            for output_index in range(output_ratio - 1, -1, -1):
                power = output_base ** (output_index)
                # extract symbol
                yield accumulator // power
                # decrement accumulator
                accumulator %= power
            # output chunk is finished, so reset the accumulator
            accumulator = 0
    '''
    if after processing all input symbols, the number of them was not divisible
    by the input ratio then we need to serialise remaining symbols from the
    accumulator then output padding symbols for the empty symbols at the end
    '''
    if input_index != 0:
        # calculate how much padding we need - this is the left over space
        padding_length = int(
            # this input index needs to be 1-indexed, but it already is
            output_ratio - ceil((input_index) / input_ratio * output_ratio)
        )
        # serialise (output ratio - padding) number of symbols
        for output_index in range(output_ratio - 1, -1 + padding_length, -1):
            power = output_base ** (output_index)
            # extract symbol
            yield accumulator // power
            # decrement accumulator
            accumulator %= power
        # yield the remaining padding symbols
        for _ in range(0, padding_length):
            yield output_base
