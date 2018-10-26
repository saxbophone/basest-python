#!/usr/bin/python
# -*- coding: utf-8 -*-


class ImproperUsageError(ValueError):
    """
    This exception is raised when an attempt is made to encode data using a
    larger output base than the input base AND when the length of the input
    data is not exactly divisible by the input ratio.

    This cannot be allowed because such options would cause data corruption.
    """
    pass


class InvalidSymbolTableError(ValueError):
    """
    This exception is raised when the symbol table and/or padding symbol
    supplied to an encoding/decoding operation are invalid.
    """
    pass
