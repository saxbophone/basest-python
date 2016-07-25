#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..core import decode, decode_raw, encode, encode_raw


class Encoder(object):
    # set out blank placeholders for class variables
    input_base = None
    output_base = None
    input_ratio = None
    output_ratio = None
    input_symbol_table = None
    output_symbol_table = None
    output_padding = None

    def encode_raw(self, input_data):
        """
        Encode raw data (no mapping of symbols). Use encode_raw function to
        actually do the work.
        """
        return encode_raw(
            input_base=self.input_base, output_base=self.output_base,
            input_ratio=self.input_ratio, output_ratio=self.output_ratio,
            input_data=input_data
        )

    def decode_raw(self, input_data):
        """
        Decode raw data (no mapping of symbols). Use decode_raw function to
        actually do the work.
        """
        return decode_raw(
            input_base=self.output_base, output_base=self.input_base,
            input_ratio=self.output_ratio, output_ratio=self.input_ratio,
            input_data=input_data
        )

    def encode(self, input_data):
        """
        Encode data. Use encode function to actually do the work.
        """
        return encode(
            input_base=self.input_base,
            input_symbol_table=self.input_symbol_table,
            output_base=self.output_base,
            output_symbol_table=self.output_symbol_table,
            output_padding=self.output_padding,
            input_ratio=self.input_ratio, output_ratio=self.output_ratio,
            input_data=input_data
        )


    def decode(self, input_data):
        """
        Decode data. Use decode function to actually do the work.
        """
        return decode(
            input_base=self.output_base,
            input_symbol_table=self.output_symbol_table,
            input_padding=self.output_padding,
            output_base=self.input_base,
            output_symbol_table=self.input_symbol_table,
            input_ratio=self.output_ratio, output_ratio=self.input_ratio,
            input_data=input_data
        )
