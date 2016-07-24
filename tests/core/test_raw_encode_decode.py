#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from ddt import data, ddt, unpack

from basest.core import raw_decode, raw_encode


@ddt
class TestRawEncodeDecode(unittest.TestCase):
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
    def test_raw_encode(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.raw_encode can encode data to an expected output given
        various base and ratio settings.
        """
        output_data = raw_encode(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

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
    def test_raw_decode(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.raw_decode can decode data an expected output given
        various base and ratio settings.
        """
        output_data = raw_decode(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

    @data(
        # Base-85 - no padding required
        (256, 85, 4, 5, [99, 97, 98, 98, 97, 103, 101, 115]),
        # Base-85 - padding is required
        (256, 85, 4, 5, [43, 42, 41, 40, 39])
    )
    @unpack
    def test_raw_encode_decode(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data
    ):
        """
        Test that basest.raw_encode can encode data that can then be decoded
        with basest.raw_decode to the same input.
        """
        # encode data
        output_data = raw_encode(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )
        # decode data
        decoded_data = raw_decode(
            input_base=output_base, output_base=input_base,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=output_data
        )

        # check data
        self.assertEqual(decoded_data, input_data)
