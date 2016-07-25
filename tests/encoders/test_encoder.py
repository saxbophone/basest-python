#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from basest.encoders import Encoder


class TestEncoderSubclass(unittest.TestCase):
    maxDiff = None

    def test_encoder_class_instantiate(self):
        """
        Test that the Encoder base class can be instantiated with no arguments.
        """
        Encoder()

    def test_encoder_subclass(
        self,
        input_base, input_symbol_table,
        output_base, output_symbol_table,
        output_padding,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that subclasses of Encoder with various different configurations
        can be created, can encode and decode data according to their formats.
        """
        # create subclass
        class CustomEncoder(Encoder):
            input_base = input_base
            input_symbol_table = input_symbol_table
            output_base = output_base
            output_symbol_table = output_symbol_table
            output_padding = output_padding
        # create instance of subclass
        instance = CustomEncoder()

        # encode some data
        output_data = instance.encode(input_data)

        # check the output
        self.assertEqual(output_data, expected_output_data)
