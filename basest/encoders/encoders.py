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
        print('RawStreamingEncoder.encode')
        # dummy implementation just yields the same input data
        for datum in data:
            yield datum

    @classmethod
    def decode(cls, data):
        print('RawStreamingEncoder.decode')
        # dummy implementation just yields the same input data
        for datum in data:
            yield datum


class MappedStreamingEncoder(RawStreamingEncoder):
    """
    Base class for generator-based encoders which operate on mapped symbols
    """
    @classmethod
    def encode(cls, data):
        print('MappedStreamingEncoder.encode')
        # wrap generator with another generator, one which maps the symbols
        for symbol in super(MappedStreamingEncoder, cls).encode(data):
            yield cls.map_input(symbol)

    @classmethod
    def decode(cls, data):
        print('MappedStreamingEncoder.decode')
        # wrap generator with another generator, one which maps the symbols
        for symbol in super(MappedStreamingEncoder, cls).decode(data):
            yield cls.map_output(symbol)

    @classmethod
    def map_input(cls, symbol):
        # dummy implementation which doesn't map anything at all
        return symbol

    @classmethod
    def map_output(cls, symbol):
        # dummy implementation which doesn't map anything at all
        return symbol


class RawEncoder(RawStreamingEncoder):
    """
    Base class for encoders which return a list of raw ints
    """
    @classmethod
    def encode(cls, data):
        print('RawEncoder.encode')
        # convert generator into list
        return list(super(RawEncoder, cls).encode(data))

    @classmethod
    def decode(cls, data):
        print('RawEncoder.decode')
        # convert generator into list
        return list(super(RawEncoder, cls).decode(data))


class Encoder(RawEncoder, MappedStreamingEncoder):
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
        print('TypedEncoder.encode')
        return super(TypedEncoder, cls).coerce_input(data)

    @classmethod
    def decode(cls, data):
        print('TypedEncoder.decode')
        return super(TypedEncoder, cls).coerce_output(data)

    @classmethod
    def coerce_input(cls, data):
        # dummy implementation that changes nothing
        return data

    @classmethod
    def coerce_output(cls, data):
        # dummy implementation that changes nothing
        return data


class EncoderTemplate(object):
    pass
