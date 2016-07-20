#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from ddt import data, ddt, unpack

from basest import decode, encode


base64_alphabet = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
)
base93_alphabet = (
    '!"#$%&\'()*+,-./0123456789:;<=>?@'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
    'abcdefghijklmnopqrstuvwxyz{|}'
)
base58_bitcoin_alphabet = (
    '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
)


@ddt
class TestEncodeDecode(unittest.TestCase):
    maxDiff = None

    @data(
        # Base-85, using just numbers for symbols - no padding required
        (
            256, range(256),
            85, range(85),
            85, 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115],
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
        ),
        # Base-85, using just numbers for symbols - padding is required
        (
            256, range(256),
            85, range(85),
            85, 4, 5,
            [43, 42, 41, 40, 39],
            [13, 74, 17, 83, 81, 12, 45, 85, 85, 85]  # TODO: Check value
        ),
        # Base-64, using most common alphabet with no padding needed
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'cabbages!']),
            list([c for c in 'Y2FiYmFnZXMh'])
        ),
        # Base-64, with a string that needs one padding symbol
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'slartybartfast']),
            list([c for c in 'c2xhcnR5YmFydGZhc3Q='])
        ),
        # Base-64, with a string that needs two padding symbols
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'belfast']),
            list([c for c in 'YmVsZmFzdA=='])
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input requiring no padding
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
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
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
        )
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
        output_data = encode(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            output_padding=output_padding,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

    @data(
        # Base-85, using just numbers for symbols - no padding
        (
            85, range(85),
            256, range(256),
            85, 5, 4,
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76],
            [99, 97, 98, 98, 97, 103, 101, 115]
        ),
        # Base-85, using just numbers for symbols - includes padding
        (
            85, range(85),
            256, range(256),
            85, 5, 4,
            [13, 74, 17, 83, 81, 12, 45, 85, 85, 85],  # TODO: Check value
            [43, 42, 41, 40, 39]
        ),
        # Base-64, using most common alphabet - no padding
        (
            64, base64_alphabet,
            256, [chr(b) for b in range(256)],
            '=', 4, 3,
            list([c for c in 'Y2FiYmFnZXMh']),
            list([c for c in 'cabbages!'])
        ),
        # Base-64, with a string that contains one padding symbol
        (
            64, base64_alphabet,
            256, [chr(b) for b in range(256)],
            '=', 4, 3,
            list([c for c in 'c2xhcnR5YmFydGZhc3Q=']),
            list([c for c in 'slartybartfast'])
        ),
        # Base-64, with a string that contains two padding symbols
        (
            64, base64_alphabet,
            256, [chr(b) for b in range(256)],
            '=', 4, 3,
            list([c for c in 'YmVsZmFzdA==']),
            list([c for c in 'belfast'])
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that has no padding
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
            ),
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing '
                        'elit. Duis eget dui non lorem tempus metus.'
                    )
                ]
            )
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding
        (
            93, base93_alphabet,
            256, [chr(b) for b in range(256)],
            '~', 115, 94,
            list(
                [
                    c for c in (
                        '<bScIZn]2oUn]4Jp=gJkWWp|h3[tysL(p:H7$`m*F|FSN+rZ`s'
                        '48,R_B:G\'+O2bR!S_{|x0~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~'  # TODO: Check this, looks fishy
                    )
                ]
            ),
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing'
                    )
                ]
            )
        )
    )
    @unpack
    def test_decode(
        self,
        input_base, input_symbol_table,
        output_base, output_symbol_table,
        input_padding, input_ratio, output_ratio,
        input_data, expected_output_data
    ):
        """
        Test that basest.decode can decode data an expected output given
        various base and ratio settings.
        """
        output_data = decode(
            input_base=input_base, input_symbol_table=input_symbol_table,
            input_padding=input_padding,
            output_base=output_base, output_symbol_table=output_symbol_table,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

    @data(
        # Base-85, using just numbers for symbols - no padding required
        (
            256, range(256),
            85, range(85),
            85, 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115]
        ),
        # Base-85, using just numbers for symbols - padding is required
        (
            256, range(256),
            85, range(85),
            85, 4, 5,
            [43, 42, 41, 40, 39]
        ),
        # Base-64, using most common alphabet with no padding needed
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'cabbages!'])
        ),
        # Base-64, with a string that needs one padding symbol
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'slartybartfast'])
        ),
        # Base-64, with a string that needs two padding symbols
        (
            256, [chr(b) for b in range(256)],
            64, base64_alphabet,
            '=', 3, 4,
            list([c for c in 'belfast'])
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input requiring no padding
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
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding
        (
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
            list(
                [
                    c for c in (
                        'Lorem ipsum dolor sit amet, consectetur adipiscing'
                    )
                ]
            )
        ),
        # Base-58, using the bitcoin alphabet. This one requires padding
        (
            256, [chr(b) for b in range(256)],
            58, base58_bitcoin_alphabet,
            '-', 8, 11,
            list(
                [
                    c for c in (
                        'Base-58 is somewhat peculiar, and does not align..!'
                    )
                ]
            )
        ),
        # Base-58, using the bitcoin alphabet. This one does not need padding
        (
            256, [chr(b) for b in range(256)],
            58, base58_bitcoin_alphabet,
            '-', 8, 11,
            list(
                [
                    c for c in (
                        'Base-58 is somewhat peculiar, and does not align'
                    )
                ]
            )
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding, and is all-zero
        (
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
            list(
                [chr(0) for _ in range(50)]
            )
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding, and is all half of max
        (
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
            list(
                [chr(127) for _ in range(50)]
            )
        ),
        # Base-93, using the base-94 alphabet with the last used for padding
        # This tests for an input that requires padding, and is all-255
        (
            256, [chr(b) for b in range(256)],
            93, base93_alphabet,
            '~', 94, 115,
            list(
                [chr(255) for _ in range(50)]
            )
        )
    )
    @unpack
    def test_encode_decode(
        self,
        input_base, input_symbol_table,
        output_base, output_symbol_table,
        output_padding,
        input_ratio, output_ratio,
        input_data
    ):
        """
        Test that basest.encode can encode data that can then be decoded with
        basest.decode to the same input.
        """
        # encode data
        output_data = encode(
            input_base=input_base, input_symbol_table=input_symbol_table,
            output_base=output_base, output_symbol_table=output_symbol_table,
            output_padding=output_padding,
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )
        # decode data
        decoded_data = decode(
            input_base=output_base, input_symbol_table=output_symbol_table,
            input_padding=output_padding,
            output_base=input_base, output_symbol_table=input_symbol_table,
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=output_data
        )

        # check data
        self.assertEqual(decoded_data, input_data)
