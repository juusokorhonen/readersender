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

class ReaderSender(object):
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
    self._logger = logger
    self._loglevel = loglevel
    self.log_format = "[{loglevel}] {msg}"

  @property
  def logger(self):
    return self._logger

  @logger.setter
  def logger(self, logger):
    self._logger = logger
    if (self.loglevel is not None):
      self._logger.setLevel(self.loglevel)
  
  @property
  def loglevel(self):
    return self._loglevel

  @loglevel.setter
  def loglevel(self, loglevel):
    self._loglevel = loglevel
    if (self.logger is not None):
      self.logger.setLevel(self._loglevel)  
  

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

  def _log_msg(self, msg, loglevel, file=sys.stdout):
    """
    Internal log formatter.
    """   
    print(self.log_format.format(msg=msg, loglevel=loglevel.upper()), file=file)
    
  def log_debug(self, msg):
    """
    Logs a debug message if debug_mode is set.
    @param[in]    msg   - Message to to be logged
    """
    if (self.logger is not None):
      self.logger.debug(msg)
    else:
      if (self.loglevel <= logging.DEBUG):
        self._log_msg(msg, 'debug')

  def log_info(self, msg):
    """
    Logs an info message to the console.
    @param[in]    msg   - Message to be logged
    """
    if (self.logger is not None):
      self.logger.info(msg)
    else:
      if (self.loglevel <= logging.INFO):
        self._log_msg(msg, 'info')

  def log_error(self, msg):
    """
    Logs an error to the console.
    @param[in]    msg   - Message to be logged
    """
    if (self.logger is not None):
      self.logger.error(msg)
    else:
      self._log_msg(msg, 'error', file=sys.stderr)
