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

from basest.core import best_ratio


@ddt
class TestBestRatio(unittest.TestCase):
    @data(
        (256, [94], range(1, 256), (94, (68, 83))),
        (256, [94], range(1, 512), (94, (458, 559))),
        (256, range(2, 95), range(1, 256), (94, (68, 83))),
        (256, range(2, 334), range(1, 256), (333, (243, 232))),
        # This is base-64's ratio, which should be 3:4
        (256, [64], range(1, 10), (64, (3, 4))),
        # This is base-85-s ratio, which should be 4:5
        (256, [85], range(1, 10), (85, (4, 5)))
    )
    @unpack
    def test_best_ratio(self, input_base, output_bases, chunk_sizes, expected):
        """
        Test that basest.best_ratio returns the correct expected outputs when
        requested to find the best compression ratios and/or base-to-base
        ratios.
        """
        self.assertEqual(
            best_ratio(input_base, output_bases, chunk_sizes), expected
        )

    @data(str, float, bytes)
    def test_invalid_inputs(self, data_type):
        """
        Any non-integer types (or lists of non-integers) passed to the function
        should raise TypeError.
        """
        with self.assertRaises(TypeError):
            best_ratio(data_type(), [2], [2])

        with self.assertRaises(TypeError):
            best_ratio(2, [data_type()], [2])

        with self.assertRaises(TypeError):
            best_ratio(2, [0, 1], [data_type()])
