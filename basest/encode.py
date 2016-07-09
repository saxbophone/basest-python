#!/usr/bin/python
# -*- coding: utf-8 -*-


def encode(
    input_base, input_symbol_table, output_base, output_symbol_table,
    output_padding, input_ratio, output_ratio, input_data
):
    """
    Encodes data from one base representation to another.
    TODO: Better docstring!
    """
    # convert input data from symbols to raw index numbers
    data = [input_symbol_table.index(symbol) for symbol in input_data]
    # this list will store the output
    encoded = list()
    for i in range(0, len(data), input_ratio):
        number = 0
        for j in range(0, input_ratio):
            number += data[i + j] * (input_base ** (input_ratio - 1 - j))
        for r in range(0, output_ratio):
            digit = number // (output_base ** (output_ratio - 1 - r))
            encoded.append(output_symbol_table[digit])
            number -= (digit * (output_base ** (output_ratio - 1 - r)))
    return encoded
