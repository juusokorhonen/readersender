#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo reader for testing.

@file           fooreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import logging
from ..reader import Reader


class FooReader(Reader):
    """A reader class that does nothing.
    @version 1.0
    """

    def connect(self):
        self.log("Connecting to foo", logging.INFO)
        return True

    def disconnect(self):
        self.log("Disconnecting from foo", logging.INFO)

    def read(self):
        data = "foo"
        self.log("Pretending to read data: {}".format(data), logging.INFO)
        return data
