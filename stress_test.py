#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import sys

from basest.core import best_ratio, decode_raw, encode_raw


def test_partial_input_with_larger_input_bases():
    # input bases in range 3..256
    for input_base in range(3, 256 + 1):
        # output bases in range 2..256
        for output_base in range(2, 256 + 1):
            # only continue if output base is not larger than input base
            if not (output_base > input_base):
                # get an encoding ratio to use
                _, ratio = best_ratio(
                    input_base,
                    [output_base],
                    range(1, 10 + 1)
                )
                # explore the whole input window
                for input_window in range(1, ratio[0] + 1):
                    '''
                    generate some random data, as many items as the partial
                    window input size that we're exploring
                    '''
                    input_data = [
                        random.randint(0, input_base - 1)
                        for _ in range(input_window)
                    ]
                    # encode the data
                    encoded_data = encode_raw(
                        input_base, output_base,
                        ratio[0], ratio[1],
                        input_data
                    )
                    # decode the data
                    decoded_data = decode_raw(
                        output_base, input_base,
                        ratio[1], ratio[0],
                        encoded_data
                    )
                    # check what we got back is the same as the original
                    assert decoded_data == input_data


if __name__ == '__main__':
    for test_function in [
        test_partial_input_with_larger_input_bases
    ]:
        print("Running '{}'".format(test_function.__name__), end='...')
        sys.stdout.flush()
        test_function()
        print('[DONE]')
