#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from ddt import data, ddt, unpack

from basest import best_ratio


@ddt
class TestBestRatio(unittest.TestCase):
    @data(
        (256, [94], range(256), (94, (92, 99))),
        (256, [94], range(512), (94, (355, 382))),
        (256, range(2, 95), range(256), (94, (92, 99))),
        (256, range(2, 333), range(256), (333, (243, 232)))
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
