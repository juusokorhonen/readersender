#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reader classes.

@file           readers.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""


import abc
import logging

import readersender

class Reader(readersender.ReaderSender):
  """
  An abstract reader class for easy interfacing.
  @version 1.3
  """
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
