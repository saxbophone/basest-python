#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class Encoder(object):
    # set out blank placeholders for class variables
    input_base = None
    output_base = None
    input_ratio = None
    output_ratio = None
    input_symbol_table = None
    output_symbol_table = None
    output_padding = None
