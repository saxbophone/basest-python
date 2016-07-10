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
    # create a 'workon' copy of the input data so we don't end up changing it
    before = list(input_data)
    # count number of padding characters
    padding_length = before.count(input_padding)
    # now, replace all padding characters with the symbol of index 0
    before = [
        (s if s != input_padding else input_symbol_table[0])
        for s in before
    ]
    # use the encode function to convert the data
    output_data = encode(
        input_base=input_base, input_symbol_table=input_symbol_table,
        output_base=output_base, output_symbol_table=output_symbol_table,
        output_padding=None,
        input_ratio=input_ratio, output_ratio=output_ratio,
        input_data=before
    )
    # strip off the unnecessary trailing zeros if there was padding
    [output_data.pop() for _ in range(padding_length)]
    '''
    HACK: If there was overlap and both bases raised to the power of their
    ratios are not equal, increment the last symbol.

    TODO: Work out why this works and thoroughly test it.
    '''
    if (
            (padding_length > 0)
            and (input_base ** input_ratio) != (output_base ** output_ratio)
    ):
        output_data[-1] = output_symbol_table[
            (output_symbol_table.index(output_data[-1]) + 1) % output_base
        ]
    return output_data
