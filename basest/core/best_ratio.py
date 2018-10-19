#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from math import ceil, log


# an easy way to store positive infinity in a manner compatible with Python 2.x
INF = float('inf')


def _encoding_ratio(base_from, base_to, chunk_sizes):
    """
    An algorithm for finding the most efficient encoding ratio
    from one base to another within a range limit.
    """
    # a ratio of 1:Infinity is the theoretical worst possible ratio
    best_ratio = (1.0, INF)
    for s in chunk_sizes:
        # validate each chunk size here
        if not isinstance(s, int):
            raise TypeError('chunk sizes must be list of ints')
        '''
        base_from ** s is the total number of values represented by the input
        base and chunk size

        base_to logarithm of this number, rounded to ceiling is the minimum
        number of symbols required in the output ratio to store this number of
        values (it might be able to store more than needed, but that doesn't
        matter)
        '''
        match = ceil(log(base_from ** s, base_to))
        # the efficiency ratio is input:output
        ratio = (float(s), match)
        # ratio efficiences can be compared by dividing them like fractions
        if (ratio[0] / ratio[1]) > (best_ratio[0] / best_ratio[1]):
            # this is the new best ratio found so far
            best_ratio = ratio
    return (int(best_ratio[0]), int(best_ratio[1]))


def best_ratio(input_base, output_bases, chunk_sizes):
    """
    For a given input base and a range of acceptable output bases and chunk
    sizes, find the most efficient encoding ratio.
    Returns the chosen output base, and the chosen encoding ratio.
    """
    # validate input base type
    if not isinstance(input_base, int):
        raise TypeError('input base must be of int type')

    # we will store the most efficient output base here
    encoder = 0
    # a ratio of 1:Infinity is the theoretical worst possible ratio
    best_ratio = (1.0, INF)
    for base_to in output_bases:
        # validate each output base here
        if not isinstance(base_to, int):
            raise TypeError('output bases must be list of ints')
        # get the best encoding ratio for this base out of all chunk sizes
        ratio = _encoding_ratio(input_base, base_to, chunk_sizes)
        # if it's more efficient, then set it as the most efficient one yet
        if (
            (float(ratio[0]) / float(ratio[1])) >
            (float(best_ratio[0]) / float(best_ratio[1]))
        ):
            best_ratio = ratio
            encoder = base_to
    # we now have the best output base and ratio for it
    return encoder, (int(best_ratio[0]), int(best_ratio[1]))
