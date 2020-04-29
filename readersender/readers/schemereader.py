#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Customizable reader for testing.

@file           schemereader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import random
import logging
import json
import datetime
from ..reader import Reader


class SchemeReader(Reader):
    """
    A reader that returns the output of a function scheme.
    @version 1.0
    """

    def __init__(self, scheme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scheme = scheme

    def connect(self):
        if self._connected:
            self.log("Already connected. Skipping.", logging.INFO)
            return
        self.log("Connecting to random reader", logging.INFO)
        self._connected = True

    def disconnect(self):
        if not self._connected:
            self.log("Already disconnected. Skipping.", logging.INFO)
            return
        self.log("Disconnecting from random reader", logging.INFO)
        self._connected = False

    def read(self):
        if not self._connected:
            raise RuntimeError("{} not connected.".format(self.__class__.__name__))
        data = self._process_scheme(self.scheme)
        self.log("Read random data: {}".format(json.dumps(data)), logging.DEBUG)
        return data

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        """Sets the scheme for the reader.
        Every field of the scheme dictionary should be a func, where func is
        a function that generates the random value.
        """
        self._scheme = scheme

    @classmethod
    def _process_scheme(cls, scheme):
        """Processes a 'scheme'.
        """
        if (isinstance(scheme, (list, tuple))):
            cnt = 0
            data = []
            for item in scheme:
                data.append(cls._process_scheme(item))
                cnt += 1
            return data
        elif (isinstance(scheme, dict)):
            data = {}
            for k, v in scheme.items():
                data[k] = cls._process_scheme(v)
            return data
        else:
            try:
                val = scheme.__call__()
                return val
            except TypeError:
                raise AttributeError("Cannot process scheme for '{}'.".format(str(scheme)))
