#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from math import ceil, log


INF = float('infinity')


def _encoding_ratio(base_from, base_to, chunk_sizes):
    """
    An algorithm for finding the most efficient encoding ratio
    from one base to another within a range limit.
    """
    best_ratio = (1.0, INF)
    for s in chunk_sizes:
        if base_from >= base_to:
            match = ceil(log(base_from ** s, base_to))
            ratio = (float(s), match)
        else:
            match = ceil(log(base_to ** s, base_from))
            ratio = (match, float(s))
        if (ratio[0] / ratio[1]) > (best_ratio[0] / best_ratio[1]):
            best_ratio = ratio
    return (int(best_ratio[0]), int(best_ratio[1]))


def best_ratio(input_base, output_bases, chunk_sizes):
    """
    For a given input base and a range of acceptable output bases and chunk
    sizes, find the most efficient encoding ratio.
    Returns the chosen output base, and the chosen encoding ratio.
    """
    encoder = 0
    best_ratio = (1.0, INF)
    for base_to in output_bases:
        ratio = _encoding_ratio(input_base, base_to, chunk_sizes)
        if (
            (float(ratio[0]) / float(ratio[1])) >
            (float(best_ratio[0]) / float(best_ratio[1]))
        ):
            best_ratio = ratio
            encoder = base_to
    return encoder, (int(best_ratio[0]), int(best_ratio[1]))
