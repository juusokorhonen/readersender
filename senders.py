#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Sender classes.

@file           senders.py
@author:        Juuso Korhonen (jk.lic at_server fw.turqoosi.net)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import abc
import logging

import readersender

class Sender(readersender.ReaderSender):
  """
  An abstract class that takes care of data processing and sending.
  @version 1.3
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, logger=None, loglevel=logging.INFO):      
    """      
    Initializes a new sender object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super(Sender, self).__init__(logger=logger, loglevel=loglevel)
    # Any custom initialization goes here or to subclasses

  @abc.abstractmethod
  def send(self, data):
    """
    Data to be sent.
    \param[in]    data    - Energy data to send
    \remarks      Implement this in subclass. 
                  Raise RuntimeError if send failed.
                  No return value
    """
    return 