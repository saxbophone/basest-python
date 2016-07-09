#!/usr/bin/python
# -*- coding: utf-8 -*-


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
    raise NotImplementedError('This function not implemented yet')
