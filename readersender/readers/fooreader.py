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
        if self._connected:
            self.log("Already connected. Skipping.", logging.INFO)
            return
        self.log("Connecting to foo", logging.INFO)
        self._connected = True

    def disconnect(self):
        if not self._connected:
            self.log("Already disconnected. Skipping.", logging.INFO)
            return
        self.log("Disconnecting from foo", logging.INFO)
        self._connected = False

    def read(self):
        if not self._connected:
            raise RuntimeError("{} not connected.".format(self.__class__.__name__))
        data = "foo"
        self.log("Pretending to read data: {}".format(data), logging.INFO)
        return data
