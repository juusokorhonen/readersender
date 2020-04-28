#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Sender classes.

@file           sender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import abc
import logging
from . import ReaderSender

class Sender(ReaderSender):
  """
  An abstract class that takes care of data processing and sending.
  @version 1.3
  """
  def __init__(self, *args, **kwargs):      
    """      
    Initializes a new sender object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super(Sender, self).__init__(*args, **kwargs)
    # Any custom initialization goes here or to subclasses


  @abc.abstractmethod
  def send(self, data):
    """
    Data to be sent.
    @param[in]    data    - Energy data to send
    @remarks      Implement this in subclass. 
                  Raise RuntimeError if send failed.
                  No return value
    """
    return 
