#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from ddt import data, ddt, unpack

from basest.core import decode_raw, encode_raw


@ddt
class TestEncodeDecodeRaw(unittest.TestCase):
    maxDiff = None

    @data(
        # Base-85 - no padding required
        (
            256, 85, 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115],
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
        ),
        # Base-85 - padding is required
        (
            256, 85, 4, 5,
            [43, 42, 41, 40, 39],
            [13, 74, 17, 83, 81, 12, 45, 85, 85, 85]
        )
    )
    @unpack
    def test_encode_raw(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.encode_raw can encode data to an expected output given
        various base and ratio settings.
        """
        output_data = encode_raw(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

    @data(str, bool, float, bytes)
    def test_encode_raw_invalid_inputs(self, data_type):
        """
        Any non-integer types (or lists of non-integers) passed to the function
        should raise TypeError.
        """
        with self.assertRaises(TypeError):
            encode_raw(
                input_base=data_type(), output_base=data_type(),
                input_ratio=data_type(), output_ratio=data_type(),
                input_data=data_type()
            )

    @data(
        # Base-85 - no padding
        (
            85, 256, 5, 4,
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76],
            [99, 97, 98, 98, 97, 103, 101, 115]
        ),
        # Base-85 - includes padding
        (
            85, 256, 5, 4,
            [13, 74, 17, 83, 81, 12, 45, 85, 85, 85],
            [43, 42, 41, 40, 39]
        )
    )
    @unpack
    def test_decode_raw(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.decode_raw can decode data an expected output given
        various base and ratio settings.
        """
        output_data = decode_raw(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

    @data(str, bool, float, bytes)
    def test_decode_raw_invalid_inputs(self, data_type):
        """
        Any non-integer types (or lists of non-integers) passed to the function
        should raise TypeError.
        """
        with self.assertRaises(TypeError):
            decode_raw(
                input_base=data_type(), output_base=data_type(),
                input_ratio=data_type(), output_ratio=data_type(),
                input_data=data_type()
            )

    @data(
        # Base-85 - no padding required
        (256, 85, 4, 5, [99, 97, 98, 98, 97, 103, 101, 115]),
        # Base-85 - padding is required
        (256, 85, 4, 5, [43, 42, 41, 40, 39])
    )
    @unpack
    def test_encode_decode_raw(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data
    ):
        """
        Test that basest.encode_raw can encode data that can then be decoded
        with basest.decode_raw to the same input.
        """
        # encode data
        output_data = encode_raw(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )
        # decode data
        decoded_data = decode_raw(
            input_base=output_base, output_base=input_base,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=output_data
        )

        # check data
        self.assertEqual(decoded_data, input_data)
