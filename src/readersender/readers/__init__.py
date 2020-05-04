#!/usr/bin/env python3
# -*- coding: utf8
import importlib

from .fooreader import FooReader
from .schemereader import SchemeReader
from .randomreader import RandomReader
if importlib.util.find_spec("serial"):
    from .serialreader import SerialReader
else:
    SerialReader = None

__all__ = [
    'FooReader',
    'SchemeReader',
    'RandomReader',
    'SerialReader'
]
