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
from . import SchemeReader


class RandomReader(Reader):
    """
    A reader that returns random values according to given scheme.
    @version 1.0
    """
    random_scheme = {
        'ts': lambda: datetime.datetime.utcnow().isoformat(),
        'd': {
            'rnd': lambda: random.random()
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheme_reader = SchemeReader(scheme=self.random_scheme, *args, **kwargs)

    @property
    def connected(self):
        return self.scheme_reader.connected

    def connect(self):
        self.scheme_reader.connect()

    def disconnect(self):
        self.scheme_reader.disconnect()

    def read(self):
        return self.scheme_reader.read()
