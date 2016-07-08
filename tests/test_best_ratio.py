#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from ddt import data, ddt, unpack

from basest import best_ratio


@ddt
class TestBestRatio(unittest.TestCase):
    @data()
    @unpack
    def test_best_ratio(self):
        best_ratio()
