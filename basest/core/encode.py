#!/usr/bin/python
# -*- coding: utf-8 -*-


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
    output_data = [output_symbol_table[0]] * output_length
    # extend the input_data to the nearest divisible length (for padding)
    before.extend([input_symbol_table[0]] * padding_length)
    # encode the data - store each group of input_ratio symbols in a number
    for i in range(0, input_nearest_length, input_ratio):
        store = 0
        for j in range(0, input_ratio):
            # get raw value of symbol
            raw_value = input_symbol_table.index(before[i + j])
            # upscale it if neccessary, in a little-endian manner
            raw_value *= (input_base ** (input_ratio - j - 1))
            # add to store
            store += raw_value
        '''
        now that store contains the value of a number of symbols, separate this
        out to the output symbols
        '''
        for j in range(0, output_ratio):
            # convert output array index
            index = ((i // input_ratio) * output_ratio) + j
            # re-interpret the number in terms of output base
            raw_value = store // (output_base ** (output_ratio - j - 1))
            # store at the calculated position, using output table
            output_data[index] = output_symbol_table[raw_value]
            # decrement the store variable, having now encoded part of it
            store -= (raw_value * (output_base ** (output_ratio - j - 1)))
    # replace padding bytes with padding character if needed
    for i in range(output_length - padding_length, output_length):
        output_data[i] = output_padding
    return output_data
