# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import absolute_import, division, print_function


class RawStreamingEncoder(object):
    """
    Base class for generator-based encoders which operate on raw ints
    """
    @classmethod
    def encode(cls, data):
        # NOTE: should be implemented in real life!
        # this method will be a generator which implements most of the
        # encoding work, yielding raw ints in the output base
        raise NotImplementedError()

    @classmethod
    def decode(cls, data):
        # NOTE: should be implemented in real life!
        # this method will be a generator which implements most of the
        # decoding work, yielding raw ints in the input base
        raise NotImplementedError()


class MappedStreamingEncoder(RawStreamingEncoder):
    """
    Base class for generator-based encoders which operate on mapped symbols
    """
    @classmethod
    def encode(cls, data):
        # wrap generator with another generator, one which maps the symbols
        for symbol in super(MappedStreamingEncoder, cls).encode(data):
            yield super(MappedStreamingEncoder, cls).map_input(symbol)

    @classmethod
    def decode(cls, data):
        # wrap generator with another generator, one which maps the symbols
        for symbol in super(MappedStreamingEncoder, cls).decode(data):
            yield super(MappedStreamingEncoder, cls).map_output(symbol)


class RawEncoder(RawStreamingEncoder):
    """
    Base class for encoders which return a list of raw ints
    """
    @classmethod
    def encode(cls, data):
        # convert generator into list
        return list(super(Encoder, cls).encode(data))

    @classmethod
    def decode(cls, data):
        # convert generator into list
        return list(super(Encoder, cls).decode(data))


class Encoder(MappedStreamingEncoder, RawEncoder):
    """
    Base class for encoders which return a list of symbols
    """
    pass


class TypedEncoder(Encoder):
    """
    Base classs for encoders which return symbols coerced to a custom type
    (for example, outputting a string rather than a list of bytes)
    """
    @classmethod
    def encode(cls, data):
        return super(TypedEncoder, cls).coerce_input(data)

    @classmethod
    def decode(cls, data):
        return super(TypedEncoder, cls).coerce_output(data)


class EncoderTemplate(object):
    pass
