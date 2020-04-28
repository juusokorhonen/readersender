#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Logger classes.

@file           loggers.py
@author:        Juuso Korhonen (jk.lic at_server fw.turqoosi.net)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import logging
import logging.handlers

class SimpleLogger(object):
    """
    Implements a simple logging class for system level logging.
    """
    def __init__(self, logger, level):
      """
      Initializes a logger with a certain logging level.
      \param[in]  logger  - A python logging instance 
      \param[in]  level   - Logging level. See the 'logging' package for information.
      """
      # Initialize to given name or the current filename
      self.logger = logger 
      self.level = level

      self.logger.info("Started logger")	
	  
    def write(self, message):
      if (message.rstrip() != ""):
        self.logger.log(self.level, message.rstrip())