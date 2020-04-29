#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ReaderSender abstract base class for readers and senders.

@file           readersender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import abc
import logging
import logging.handlers


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
        self._loggers = [logger or logging.getLogger(__name__)]
        self._loggers[0].setLevel(loglevel)

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

    @abc.abstractmethod
    def connect(self):
        """Connects a reader/sender to source/target.
        Usually called after init.
        """
        return

    @abc.abstractmethod
    def disconnect(self):
        """Disconnects from the server.
        """
        return

    def log(self, msg, loglevel):
        """Logs to all loggers a msg with given loglevel.
        """
        for logger in self.loggers:
            logger.log(loglevel, msg)
