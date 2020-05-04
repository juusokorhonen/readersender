#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ReaderSender abstract base class for readers and senders.

@file           readersender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import abc
import sys
import logging
import logging.handlers
from .helpers import only_connected, only_disconnected


class ReaderSender(object, metaclass=abc.ABCMeta):
    """An abstract ReaderSender class.
    Takes care of some basic functionality and interfaces.
    @version  1.0
    """
    def __init__(self, logger=None, loglevel=logging.INFO):
        """Initializes a new ReaderSender object.
        After initialization, you can set eg. debug_mode, silent_mode, and log_format
        parameter.
        """
        if logger is not None:
            self._loggers = [logger.getChild(__class__.__name__)]
        else:
            self._loggers = [logging.getLogger(__class__.__name__)]
            self._loggers[0].addHandler(logging.StreamHandler(sys.stdout))
        self._loggers[0].setLevel(loglevel)

        self._connected = False

    @property
    def logger(self):
        """Returns the default logger.
        """
        return self._loggers[0]

    @logger.setter
    def logger(self, logger):
        """Replaces the default logger.
        """
        if logger is not None:
            self._loggers[0] = logger

    @property
    def loggers(self):
        """Returns a list of all registered loggers.
        """
        return self._loggers

    @property
    def connected(self):
        return self._connected

    @only_disconnected(action='pass')
    def connect(self):
        """Connects a reader/sender to source/target.
        Usually called after init.
        """
        self._connected = True

    @only_connected(action='pass')
    def disconnect(self):
        """Disconnects from the server.
        """
        self._connected = False

    def log(self, msg, loglevel):
        """Logs to all loggers a msg with given loglevel.
        """
        for logger in self.loggers:
            logger.log(loglevel, "{}".format(msg))

    # Context Manager implementation
    def __enter__(self):
        """Initializes the context by opening the connection.

        Notes
        -----
        Usage example:
            with ReaderSender() as rs:
                rs.connect()
                if rs.connected:
                    print("Connected.")
        """
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        """Takes care of closing connections automatically.
        """
        if self.connected:
            self.disconnect()
        return True
