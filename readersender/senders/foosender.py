#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo sender for testing.

@file           foosender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import logging
import sys
from ..sender import Sender


class FooSender(Sender):
    """A sender class that does nothing.
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

    def send(self, data):
        """Sends data to sys.stdout.
        """
        if not self._connected:
            raise RuntimeError("{} not connected.".format(self.__class__.__name__))
        self.log("Sending (not really) data: {}".format(data), logging.INFO)
        sys.stdout.write(data)
