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
            self.log("{} already connected. Skipping.".format(self.__class__.__name__), logging.INFO)
            return
        self.log("Connecting {}.".format(self.__class__.__name__), logging.INFO)
        self._connected = True

    def disconnect(self):
        if not self._connected:
            self.log("{} already disconnected. Skipping.".format(self.__class__.__name__), logging.INFO)
            return
        self.log("Disconnecting {}.".format(self.__class__.__name__), logging.INFO)
        self._connected = False

    def send(self, data):
        """Sends data to sys.stdout.
        """
        if not self._connected:
            raise RuntimeError("{} not connected.".format(self.__class__.__name__))
        self.log("{} sending data.".format(self.__class__.__name__), logging.INFO)
        sys.stdout.write(str(data) + "\n")
