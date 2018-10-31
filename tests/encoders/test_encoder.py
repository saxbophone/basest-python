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
from mock import patch

from basest.encoders import Encoder


base64_alphabet = [
    s for s in
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
]
base93_alphabet = [
    s for s in
    '!"#$%&\'()*+,-./0123456789:;<=>?@'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
    'abcdefghijklmnopqrstuvwxyz{|}'
]


@ddt
class TestEncoderSubclass(unittest.TestCase):
    maxDiff = None

    def make_custom_encoder_subclass(self, **kwargs):
        """
        Given keyword-arguments of the values of class variables to use, create
        and return a custom subclass of Encoder.
        """
        # sanity checking - do we have all the mandatory class variables?
        mandatory = {
            'input_base', 'output_base', 'input_ratio', 'output_ratio',
        }

        if not mandatory.issubset(kwargs):
            raise ValueError('Missing required class variables to set.')

        class CustomEncoder(Encoder):
            input_base = kwargs['input_base']
            output_base = kwargs['output_base']
            input_ratio = kwargs['input_ratio']
            output_ratio = kwargs['output_ratio']
            input_symbol_table = (
                kwargs['input_symbol_table'] if 'input_symbol_table' in kwargs
                else Encoder.input_symbol_table
            )
            output_symbol_table = (
                kwargs['output_symbol_table']
                if 'output_symbol_table' in kwargs
                else Encoder.output_symbol_table
            )
            padding_symbol = (
                kwargs['padding_symbol'] if 'padding_symbol' in kwargs
                else Encoder.padding_symbol
            )
        return CustomEncoder

    def test_make_custom_encoder_subclass(self):
        """
        Test helper method make_custom_encoder_subclass can create new
        subclasses of Encoder with all class variables overridden.
        """
        rough_base64_alphabet = [
            chr(33 + c) if c != '=' else '~' for c in range(64)
        ]
        custom_class = self.make_custom_encoder_subclass(
            input_base=256, output_base=64, input_ratio=3, output_ratio=4,
            input_symbol_table=[chr(c) for c in range(256)],
            output_symbol_table=rough_base64_alphabet,
            padding_symbol='='
        )

        # check class attributes
        self.assertEqual(custom_class.input_base, 256)
        self.assertEqual(custom_class.output_base, 64)
        self.assertEqual(custom_class.input_ratio, 3)
        self.assertEqual(custom_class.output_ratio, 4)
        self.assertEqual(
            custom_class.input_symbol_table, [chr(c) for c in range(256)]
        )
        self.assertEqual(
            custom_class.output_symbol_table, rough_base64_alphabet
        )
        self.assertEqual(
            custom_class.padding_symbol, '='
        )

    def test_make_custom_encoder_subclass_minimum(self):
        """
        Test helper method make_custom_encoder_subclass can create new
        subclasses of Encoder with only required class variables overridden.
        """
        custom_class = self.make_custom_encoder_subclass(
            input_base=256, output_base=64, input_ratio=3, output_ratio=4
        )

        # check class attributes
        self.assertEqual(custom_class.input_base, 256)
        self.assertEqual(custom_class.output_base, 64)
        self.assertEqual(custom_class.input_ratio, 3)
        self.assertEqual(custom_class.output_ratio, 4)

    @data(
        {
            'output_base': 64,
            'input_ratio': 3,
            'output_ratio': 4,
        },
        {
            'input_base': 256,
            'input_ratio': 3,
            'output_ratio': 4,
        },
        {
            'input_base': 256,
            'output_base': 64,
            'output_ratio': 4,
        },
        {
            'input_base': 256,
            'output_base': 64,
            'input_ratio': 3,
        },
    )
    def test_make_custom_encoder_subclass_error(self, options):
        """
        Test helper method make_custom_encoder_subclass should raise ValueError
        if called with missing required arguments.
        """
        with self.assertRaises(ValueError):
            self.make_custom_encoder_subclass(**options)

    def test_encoder_class_instantiate(self):
        """
        Test that the Encoder base class can be instantiated with no arguments.
        """
        Encoder()

    @data(
        (256, 64, 3, 4, [1, 234, 56, 183, 97, 67, 33, 3]),
        (256, 16, 1, 2, [3, 5, 7, 11, 13, 17, 19, 23, 29])
    )
    @unpack
    @patch('basest.encoders.encoder.encode_raw')
    def test_encoder_subclass_encode_raw(
        self, input_base, output_base,
        input_ratio, output_ratio, input_data,
        m_encode_raw
    ):
        """
        Test that subclasses of Encoder with various different configurations
        can be created, and that Encoder().encode_raw calls
        basest.core.encode_raw() with the correct arguments, and returns what
        that function returns.
        """
        # mock return value of encode_raw
        m_encode_raw.return_value = 'fish'
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # call instance method encode_raw() with input data
        result = CustomEncoder().encode_raw(input_data)

        # check the library function was called
        m_encode_raw.assert_called_once_with(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )
        # check that the method returned whatever the function did
        self.assertEqual(result, m_encode_raw.return_value)

    @data(
        (64, 256, 4, 3, [24, 54, 13, 35, 24, 48, 64, 64]),
        (16, 256, 2, 1, [1, 7, 13, 15, 12, 0, 1, 16])
    )
    @unpack
    @patch('basest.encoders.encoder.decode_raw')
    def test_encoder_subclass_decode_raw(
        self, input_base, output_base,
        input_ratio, output_ratio, input_data,
        m_decode_raw
    ):
        """
        Test that subclasses of Encoder with various different configurations
        can be created, and that Encoder().decode_raw calls
        basest.core.decode_raw() with the correct arguments, and returns what
        that function returns.
        """
        # mock return value of decode_raw
        m_decode_raw.return_value = 'boat'
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # call instance method decode_raw() with input data
        result = CustomEncoder().decode_raw(input_data)

        # check the library function was called
        m_decode_raw.assert_called_once_with(
            input_base=output_base, output_base=input_base,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=input_data
        )
        # check that the method returned whatever the function did
        self.assertEqual(result, m_decode_raw.return_value)

    @data(
        # Base-64
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'cabbages!'])
        ),
        # Base-93
        (
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing '
                        'elit. Duis eget dui non lorem tempus metus.'
                    )
                ]
            )
        )
    )
    @unpack
    @patch('basest.encoders.encoder.encode')
    def test_encoder_subclass_encode(
        self, input_base, input_symbol_table,
        output_base, output_symbol_table, padding_symbol,
        input_ratio, output_ratio, input_data,
        m_encode
    ):
        """
        Test that subclasses of Encoder with various different configurations
        can be created, and that Encoder().encode calls basest.core.encode()
        with the correct arguments, and returns what that function returns.
        """
        # mock return value of encode
        m_encode.return_value = 'Albatross'
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            padding_symbol=padding_symbol,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # call instance method encode() with input data
        result = CustomEncoder().encode(input_data)

        # check the library function was called
        m_encode.assert_called_once_with(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            output_padding=padding_symbol,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )
        # check that the method returned whatever the function did
        self.assertEqual(result, m_encode.return_value)

    @data(
        # Base-64
        (
            64, base64_alphabet,
            256, [chr(b) for b in range(256)],
            '=', 4, 3,
            list([c for c in 'Y2FiYmFnZXMh'])
        ),
        # Base-93
        (
            93, base93_alphabet,
            256, [chr(b) for b in range(256)],
            '~', 115, 94,
            list(
                [
                    c for c in (
                        '<bScIZn]2oUn]4Jp=gJkWWp|h3[tysL(p:H7$`m*F|FSN+rZ`s4'
                        '8,R_B:G\'+O8.!+VCj(VNBp</:S!A&W-mA2<rCO5LIAAa+flHJ@'
                        'yXj^m0VH8"0G9B'
                    )
                ]
            )
        )
    )
    @unpack
    @patch('basest.encoders.encoder.decode')
    def test_encoder_subclass_decode(
        self, input_base, input_symbol_table,
        output_base, output_symbol_table, padding_symbol,
        input_ratio, output_ratio, input_data,
        m_decode
    ):
        """
        Test that subclasses of Encoder with various different configurations
        can be created, and that Encoder().decode calls
        basest.core.decode() with the correct arguments, and returns what that
        function returns.
        """
        # mock return value of decode
        m_decode.return_value = 'Vauxhall'
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, input_symbol_table=input_symbol_table,
            padding_symbol=padding_symbol,
            output_base=output_base, output_symbol_table=output_symbol_table,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # call instance method decode() with input data
        result = CustomEncoder().decode(input_data)

        # check the library function was called
        m_decode.assert_called_once_with(
            input_base=output_base, input_symbol_table=output_symbol_table,
            input_padding=padding_symbol,
            output_base=input_base, output_symbol_table=input_symbol_table,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=input_data
        )
        # check that the method returned whatever the function did
        self.assertEqual(result, m_decode.return_value)
