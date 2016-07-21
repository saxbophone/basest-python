#!/usr/bin/python
# -*- coding: utf-8 -*-
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
