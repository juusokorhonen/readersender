#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reader classes.

@file           reader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import abc
from . import ReaderSender


class Reader(ReaderSender):
    """An abstract reader class for easy interfacing.
    Defines methods to be implemented in subclasses.
    @version 1.4
    """
    @abc.abstractmethod
    def read(self):
        """Reads data from the reader.
        Subclasses should implement their own methods with optional arguments.
        @returns Read data
        """
        return None
