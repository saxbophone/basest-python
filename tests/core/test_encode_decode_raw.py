# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from ddt import data, ddt, unpack

from basest.core import decode_raw, encode_raw
from basest.exceptions import ImproperUsageError, InvalidInputLengthError


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
        (94, 256, 10, 9, [1, 2, 3, 4, 5]),
        (94, 256, 10, 9, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
        (78, 256, 20, 16, [70]),
        (78, 256, 20, 16, [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
    )
    @unpack
    def test_encode_raw_invalid_input_ratio(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data
    ):
        """
        When encoding from a smaller base to a larger one, it is impossible to
        encode input if the number of symbols is not an exact multiple of the
        input ratio. This is because such an action normally can be solved with
        padding, however padding can only be used successfully on the 'smaller'
        side of the transformation, in any other case data corruption occurs.
        If this is attempted, then ImproperUsageError should be raised.
        """
        with self.assertRaises(ImproperUsageError):
            encode_raw(
                input_base=input_base, output_base=output_base,
                input_ratio=input_ratio, output_ratio=output_ratio,
                input_data=input_data
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
        # Base-85 - padding has been truncated, which means it is too short!
        (
            85, 256, 5, 4,
            [13, 74, 17, 83, 81, 12, 45]
        )
    )
    @unpack
    def test_decode_raw_rejects_input_of_incorrect_length(
        self,
        input_base, output_base,
        input_ratio, output_ratio,
        input_data
    ):
        """
        When decode_raw() is called with input data which is not of a length
        exactly divisible by the input ratio, InvalidInputLengthError should be
        raised.
        """
        with self.assertRaises(InvalidInputLengthError):
            decode_raw(
                input_base=input_base, output_base=output_base,
                input_ratio=input_ratio, output_ratio=output_ratio,
                input_data=input_data
            )

    @data(
        # Base-85 - no padding required
        (256, 85, 4, 5, [99, 97, 98, 98, 97, 103, 101, 115]),
        # Base-85 - padding is required
        (256, 85, 4, 5, [43, 42, 41, 40, 39]),
        # Base-94 to Base-256 --the 'wrong' way round, but it is valid as long
        # as the input data is a multiple of the input_ratio size.
        # Otherwise, padding-related errors occur (because padding happens on
        # the 'smaller' side of the transformation only).
        (94, 256, 10, 9, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
        (94, 256, 10, 9, [93, 88, 77, 66, 55, 44, 33, 22, 11, 0])
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
