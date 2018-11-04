# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import (
    absolute_import, division, print_function
)

import pytest

from basest.encoders import Encoder


# some constants which are handy for making various different encoders
ALL_BYTES = list(range(256))

BASE_64_ALPHABET = list(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
)
BASE_64_PADDING = '='

# NOTE: this is the RFC 4648 Base32 alphabet
BASE_32_ALPHABET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
BASE_32_PADDING = '='


class TestEncoder(object):
    def build_custom_encoder(
        self,
        arg_input_base,
        arg_output_base,
        arg_encoding_ratio,
        arg_input_alphabet,
        arg_output_alphabet,
        arg_output_padding
    ):
        """
        Test helper method, returns a new Encoder subclass with the class
        attributes set as the named parameters of this method.
        """
        class CustomEncoder(Encoder):
            input_base = arg_input_base
            output_base = arg_output_base
            encoding_ratio = arg_encoding_ratio
            input_alphabet = arg_input_alphabet
            output_alphabet = arg_output_alphabet
            output_padding = arg_output_padding

        return CustomEncoder

    @pytest.mark.parametrize(
        'input_data,expected_output',
        [
            (
                list(b'cabbages'),
                list('Y2FiYmFnZXM=')
            ),
            (
                list(b'basest-python is pretty neat!'),
                list('YmFzZXN0LXB5dGhvbiBpcyBwcmV0dHkgbmVhdCE=')
            ),
            (
                list(range(256)),
                list(
                    'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpK'
                    'issLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVF'
                    'VWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+'
                    'AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmq'
                    'q6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1'
                    'dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w'
                    '=='
                ),
            ),
            (
                list(reversed(range(256))),
                list(
                    '//79/Pv6+fj39vX08/Lx8O/u7ezr6uno5+bl5OPi4eDf3t3c29rZ2NfW1'
                    'dTT0tHQz87NzMvKycjHxsXEw8LBwL++vby7urm4t7a1tLOysbCvrq2sq6'
                    'qpqKempaSjoqGgn56dnJuamZiXlpWUk5KRkI+OjYyLiomIh4aFhIOCgYB'
                    '/fn18e3p5eHd2dXRzcnFwb25tbGtqaWhnZmVkY2JhYF9eXVxbWllYV1ZV'
                    'VFNSUVBPTk1MS0pJSEdGRURDQkFAPz49PDs6OTg3NjU0MzIxMC8uLSwrK'
                    'ikoJyYlJCMiISAfHh0cGxoZGBcWFRQTEhEQDw4NDAsKCQgHBgUEAwIBAA'
                    '=='
                )
            )
        ]
    )
    def test_base64_encoding(self, input_data, expected_output):
        """
        Test that a base64 encoder created by subclassing the Encoder class
        encodes data properly.
        """
        Base64Encoder = self.build_custom_encoder(
            256,
            64,
            (3, 4),
            ALL_BYTES,
            BASE_64_ALPHABET,
            BASE_64_PADDING
        )

        output = Base64Encoder.encode(input_data)

        assert output == expected_output
