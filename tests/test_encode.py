#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from ddt import data, ddt, unpack

from basest import encode


@ddt
class TestEncode(unittest.TestCase):
    @data(
        # Base-85, using just numbers for symbols
        (
            256, range(256), 85, range(85), 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115],
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
        ),
        # Base-64, using most common alphabet with no padding
        (
            256, [chr(b) for b in range(256)],
            64,
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
            3, 4,
            list([c for c in 'cabbages!']), list([c for c in 'Y2FiYmFnZXMh'])
        )
    )
    @unpack
    def test_encode(
        self, input_base, input_symbol_table, output_base, output_symbol_table,
        input_ratio, output_ratio, input_data, expected_output_data
    ):
        """
        Test that basest.encode can encode data to an expected output given
        various base and ration settings and that it can also decode the output
        back to the original input.
        """
        output_data = encode(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

        decoded_data = encode(
            input_base=output_base, input_symbol_table=output_symbol_table,
            output_base=input_base, output_symbol_table=input_symbol_table,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=output_data
        )

        self.assertEqual(decoded_data, input_data)
