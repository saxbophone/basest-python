#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from ddt import data, ddt, unpack

from basest import encode

base64_alphabet = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
)
base93_alphabet = (
    '!"#$%&\'()*+,-./0123456789:;<=>?@'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
    'abcdefghijklmnopqrstuvwxyz{|}'
)


@ddt
class TestEncode(unittest.TestCase):
    @data(
        # Base-85, using just numbers for symbols - no padding required
        (
            256, range(256), 85, range(85), 85, 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115],
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
        ),
        # Base-85, using just numbers for symbols - padding is required
        (
            256, range(256), 85, range(85), 85, 4, 5,
            [43, 42, 41, 40, 39],
            [13, 74, 17, 83, 81, 12, 45, 85, 85, 85]  # TODO: Check value
        ),
        # Base-64, using most common alphabet with no padding needed
        (
            256, [chr(b) for b in range(256)], 64, base64_alphabet, '=', 3, 4,
            list([c for c in 'cabbages!']), list([c for c in 'Y2FiYmFnZXMh'])
        ),
        # Base-64, with a string that needs one padding symbol
        (
            256, [chr(b) for b in range(256)], 64, base64_alphabet, '=', 3, 4,
            list([c for c in 'slartybartfast']),
            list([c for c in 'c2xhcnR5YmFydGZhc3Q='])
        ),
        # Base-64, with a string that needs two padding symbols
        (
            256, [chr(b) for b in range(256)], 64, base64_alphabet, '=', 3, 4,
            list([c for c in 'belfast']),
            list([c for c in 'YmVsZmFzdA=='])
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input requiring no padding
        (
            256, [chr(b) for b in range(256)], 93, base93_alphabet, '~',
            94, 115,
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing '
                        'elit. Duis eget dui non lorem tempus metus.'
                    )
                ]
            ),
            list(
                [
                    c for c in (
                        '<bScIZn]2oUn]4Jp=gJkWWp|h3[tysL(p:H7$`m*F|FSN+rZ`s4'
                        '8,R_B:G\'+O8.!+VCj(VNBp</:S!A&W-mA2<rCO5LIAAa+flHJ@'
                        'yXj^m0VH8"0G9B'
                    )
                ]
            )
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding
        (
            256, [chr(b) for b in range(256)], 93, base93_alphabet, '~',
            94, 115,
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing'
                    )
                ]
            ),
            list(
                [
                    c for c in (
                        '<bScIZn]2oUn]4Jp=gJkWWp|h3[tysL(p:H7$`m*F|FSN+rZ`s'
                        '48,R_B:G\'+O2bR!S_{|x0~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~'  # TODO: Check this, looks fishy
                    )
                ]
            )
        ),
    )
    @unpack
    def test_encode(
        self,
        input_base, input_symbol_table,
        output_base, output_symbol_table,
        output_padding,
        input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.encode can encode data to an expected output given
        various base and ratio settings.
        """
        self.maxDiff = None
        output_data = encode(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            output_padding=output_padding,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)
