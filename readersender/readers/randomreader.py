#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Random value reader for testing.

@file           randomreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import random
import logging
import json
import datetime
from ..reader import Reader


class RandomReader(Reader):
    """
    A reader that returns random values according to given scheme.
    @version 1.0
    """

    def __init__(self, scheme=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if (scheme is None):
            # Use a default scheme
            scheme = {
                'ts': lambda: datetime.datetime.utcnow().isoformat(),
                'd': {
                    'rnd': lambda: random.random()
                }
            }

        self.scheme = scheme

    def connect(self):
        self.log("Connecting to random reader", logging.INFO)
        return True

    def disconnect(self):
        self.log("Disconnecting from random reader", logging.INFO)

    def read(self):
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

    def _process_scheme(self, scheme):
        """Processes a 'scheme'.
        """
        if (isinstance(scheme, (list, tuple))):
            cnt = 0
            data = []
            for item in scheme:
                data.append(self._process_scheme(item))
                cnt += 1
            return data
        elif (isinstance(scheme, dict)):
            data = {}
            for k, v in scheme.items():
                data[k] = self._process_scheme(v)
            return data
        else:
            try:
                val = scheme()
                return val
            except TypeError:
                return str(scheme)
