#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ReaderSender abstract base class for readers and senders.

@file           readersender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import sys
import abc
import logging
import logging.handlers

class ReaderSender(object, metaclass=abc.ABCMeta):
  """
  An abstract class that takes care of some basic functionality and interfaces.
  @version  1.0
  """
  def __init__(self, logger=None, loglevel=logging.INFO):      
    """      
    Initializes a new ReaderSender object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    self._logger = logger or logging.getLogger(__name__)
    self._loglevel = loglevel


  @property
  def logger(self):
    return self._logger


  @logger.setter
  def logger(self, logger):
    self._logger = logger
    self._logger.setLevel(self._loglevel)
  

  @abc.abstractmethod
  def connect(self):
    """
    Connect to reader/sender. Usually called after init.
    """  
    return


  @abc.abstractmethod
  def disconnect(self):
    """
    Disconnect from the server.
    """
    return


  def log(self, msg, loglevel):
    """
    Log msg with given loglevel.
    """   
    self.logger.log(loglevel, msg)
  
