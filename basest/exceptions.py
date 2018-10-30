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


class InvalidSymbolTableError(ValueError):
    """
    This exception is raised when the symbol table and/or padding symbol
    supplied to an encoding/decoding operation are invalid.
    """
    pass


class InvalidInputError(ValueError):
    """
    This exception is raised when an encoding or decoding function receives
    input data containing symbols which are not in the relevant symbol table.
    """
    pass


class ImproperUsageError(ValueError):
    """
    This exception is raised when an attempt is made to encode data using a
    larger output base than the input base AND when the length of the input
    data is not exactly divisible by the input ratio.

    This cannot be allowed because such options would cause data corruption.
    """
    pass


class InvalidInputLengthError(ValueError):
    """
    This exception is raised when an attempt is made to decode data which is
    not the correct length (e.g. where the length is not an exact multiple of
    the input ratio).

    This exception is only valid when performing a decoding operation, as data
    to be encoded is permitted to be shorter than the input ratio as long as
    the output base is smaller than the input base.
    """
    pass
