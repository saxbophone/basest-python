#!/usr/bin/python
# -*- coding: utf-8 -*-


class InvalidSymbolTableError(ValueError):
    """
    This exception being raised indicates that the symbol table and/or padding
    symbol supplied to an encoding/decoding operation are invalid.
    """
    pass
