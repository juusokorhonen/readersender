#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reader classes.

@file           readers.py
@author:        Juuso Korhonen (jk.lic at_server fw.turqoosi.net)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import abc
import logging

import readersender

class Reader(readersender.ReaderSender):
  """
  An abstract reader class for easy interfacing.
  @version 1.3
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, logger=None, loglevel=logging.INFO):      
    """      
    Initializes a new reader object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super(Reader, self).__init__(logger=logger, loglevel=loglevel)
    # Any custom initialization goes here or to subclasses

  @abc.abstractmethod
  def read(self):
    """
    Reads data from the reader. Subclasses should implement their own methods with optional arguments.
    @returns Read data
    """
    return None
