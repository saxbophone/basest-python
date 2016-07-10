#!/usr/bin/python
# -*- coding: utf-8 -*-
from .encode import encode


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
    input_length = len(input_data)
    overlap = input_length % input_ratio
    # first, check if the input data is not long enough and pad it if it isn't
    if overlap > 0:
        ...
    # count number of padding characters
    padding_length = input_data.count(input_padding)
    # now, replace all padding characters with the symbol of index 0
    input_data = [
        (s if s != input_padding else input_symbol_table[0])
        for s in input_data
    ]
    # use the encode function to convert the data
    output_data = encode(
        input_base=input_base, input_symbol_table=input_symbol_table,
        output_base=output_base, output_symbol_table=output_symbol_table,
        output_padding=None,
        input_ratio=input_ratio, output_ratio=output_ratio,
        input_data=input_data
    )
    # strip off the unnecessary trailing zeros if there was padding
    [output_data.pop() for _ in range(padding_length)]
    return output_data
