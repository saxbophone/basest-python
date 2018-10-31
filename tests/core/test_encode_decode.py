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

from basest.core import decode, encode
from basest.exceptions import InvalidInputError, InvalidSymbolTableError


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
base58_bitcoin_alphabet = [
    s for s in
    '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
]


@ddt
class TestEncodeDecode(unittest.TestCase):
    maxDiff = None

    @data(
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
                        '~~~~~~~~~~~~~~~~'
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
        (list('abcd'), list('ccccc'), '1'),
        (list('!!!!!'), list('abcdef'), '#')
    )
    @unpack
    def test_encode_rejects_non_unique_symbol_tables(
        self,
        input_symbol_table,
        output_symbol_table,
        padding_symbol
    ):
        """
        When a non-unique input or output symbol table is passed to encode(),
        InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            encode(
                len(input_symbol_table), input_symbol_table,
                len(output_symbol_table), output_symbol_table,
                padding_symbol,
                1, 1,
                []
            )

    def test_encode_rejects_output_symbol_table_containing_padding_symbol(
        self
    ):
        """
        When the output symbol table passed to encode() contains the padding
        symbol, InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            encode(1, ['a'], 1, ['b'], 'b', 1, 1, [])

    @data(
        (list('abcd'), list('efghijk'), None),
        (list('1234'), [1, 2, 3, None], '#'),
        ([None, 2, 3, 4], list('cabuges'), '#')
    )
    @unpack
    def test_encode_rejects_none_used_in_symbol_tables_and_padding(
        self,
        input_symbol_table,
        output_symbol_table,
        padding_symbol
    ):
        """
        When any of the symbol tables or the padding symbol passed to encode()
        are or contain None, InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            encode(
                len(input_symbol_table), input_symbol_table,
                len(output_symbol_table), output_symbol_table,
                padding_symbol,
                1, 1,
                []
            )

    @data(
        ([0, 1, 2, 3], [0, 1, 4])
    )
    @unpack
    def test_encode_rejects_symbols_not_found_in_symbol_table(
        self,
        input_symbols,
        input_symbol_table
    ):
        """
        When the encode() function is called with input data that contains
        symbols which are not found in the input symbol table,
        InvalidInputError should be raised.
        """
        with self.assertRaises(InvalidInputError):
            encode(
                4, input_symbol_table,
                8, list(range(8)),
                'P',
                2, 3,
                input_symbols
            )

    @data(
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
                        '~~~~~~~~~~~~~~~~'
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
        (list('abcd'), list('ccccc'), '1'),
        (list('!!!!!'), list('abcdef'), '#')
    )
    @unpack
    def test_decode_rejects_non_unique_symbol_tables(
        self,
        input_symbol_table,
        output_symbol_table,
        padding_symbol
    ):
        """
        When a non-unique input or output symbol table is passed to decode(),
        InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            decode(
                len(input_symbol_table), input_symbol_table,
                padding_symbol,
                len(output_symbol_table), output_symbol_table,
                1, 1,
                []
            )

    def test_decode_rejects_input_symbol_table_containing_padding_symbol(
        self
    ):
        """
        When the input symbol table passed to decode() contains the padding
        symbol, InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            decode(1, ['a'], 'a', 1, ['b'], 1, 1, [])

    @data(
        (list('abcd'), list('efghijk'), None),
        (list('1234'), [1, 2, 3, None], '#'),
        ([None, 2, 3, 4], list('cabuges'), '#')
    )
    @unpack
    def test_decode_rejects_none_used_in_symbol_tables_and_padding(
        self,
        input_symbol_table,
        output_symbol_table,
        padding_symbol
    ):
        """
        When any of the symbol tables or the padding symbol passed to decode()
        are or contain None, InvalidSymbolTableError should be raised.
        """
        with self.assertRaises(InvalidSymbolTableError):
            decode(
                len(input_symbol_table), input_symbol_table,
                padding_symbol,
                len(output_symbol_table), output_symbol_table,
                1, 1,
                []
            )

    @data(
        ([0, 1, 2, 3], [0, 1, 4])
    )
    @unpack
    def test_decode_rejects_symbols_not_found_in_symbol_table(
        self,
        input_symbols,
        input_symbol_table
    ):
        """
        When the decode() function is called with input data that contains
        symbols which are not found in the input symbol table,
        InvalidInputError should be raised.
        """
        with self.assertRaises(InvalidInputError):
            decode(
                4, input_symbol_table,
                'P',
                8, list(range(8)),
                3, 2,
                input_symbols
            )

    @data(
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
