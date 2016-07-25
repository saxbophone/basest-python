#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from ddt import data, ddt, unpack
from mock import patch

from basest.encoders import Encoder


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
            output_padding = (
                kwargs['output_padding'] if 'output_padding' in kwargs
                else Encoder.output_padding
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
            output_padding='='
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
            custom_class.output_padding, '='
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
        basest.core.encode_raw() with the correct arguments.
        """
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # raw instance method encode_raw() with input data
        CustomEncoder().encode_raw(input_data)

        # check the library function was called
        m_encode_raw.assert_called_once_with(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

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
        basest.core.decode_raw() with the correct arguments.
        """
        # create subclass
        CustomEncoder = self.make_custom_encoder_subclass(
            input_base=input_base, output_base=output_base,
            input_ratio=input_ratio, output_ratio=output_ratio
        )

        # raw instance method encode_raw() with input data
        CustomEncoder().decode_raw(input_data)

        # check the library function was called
        m_decode_raw.assert_called_once_with(
            input_base=output_base, output_base=input_base,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=input_data
        )
