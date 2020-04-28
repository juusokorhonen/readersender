#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reader classes.

@file           reader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import abc
import logging
from . import ReaderSender


class Reader(ReaderSender):
  """
  An abstract reader class for easy interfacing.
  @version 1.3
  """
  def __init__(self, *args, **kwargs):      
    """      
    Initializes a new reader object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super().__init__(*args, **kwargs)
    # Any custom initialization goes here or to subclasses

  @abc.abstractmethod
  def read(self):
    """
    Reads data from the reader. Subclasses should implement their own methods with optional arguments.
    @returns Read data
    """
    return None
