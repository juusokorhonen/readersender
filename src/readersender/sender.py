#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Sender classes.

@file           sender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
from . import ReaderSender
from .helpers import only_connected


class Sender(ReaderSender):
    """An abstract class that takes care of data processing and sending.
    @version 1.3
    """
    @only_connected(action='warn')
    def send(self, data):
        """Send data.
        @param[in]    data    - Data to send
        @remarks      Implement this in subclass.
                      Raise RuntimeError if send failed.
                      No return value
        """
        pass
