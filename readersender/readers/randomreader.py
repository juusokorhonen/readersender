#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Random value reader for testing.

@file           randomreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""


import abc
import random
import logging
import json
import datetime

import readers

class RandomReader(readers.Reader):
  """
  A reader that returns random values according to given scheme.
  @version 1.0
  """

  def __init__(self, scheme=None, logger=None, loglevel=logging.INFO):
    super(RandomReader, self).__init__(logger=logger, loglevel=loglevel)

    if (scheme is None):
      # Use a default scheme
      scheme = {
        'ts': lambda: datetime.datetime.utcnow().isoformat(),
        'd': {
          'rnd': lambda: random.random()
        }
      }

    self.scheme = scheme

  def connect(self):
    self.log_debug("Connecting to random reader")
    return True

  def disconnect(self):
    self.log_debug("Disconnecting from random reader")

  def read(self):
    data = self._process_scheme(self.scheme)
    self.log_debug("Read random data: {}".format(json.dumps(data)))
    return data

  @property
  def scheme(self):
      return self._scheme
  
  @scheme.setter
  def scheme(self, scheme):
    """
    Sets the scheme for the reader. Every field of the scheme dictionary should be a func, where func is the function 
    that generates the random value.
    """
    self._scheme = scheme

  def _process_scheme(self, scheme):
    """
    @remarks   Modifies 'scheme', so make sure to send in a copy!
    """
    if (isinstance(scheme, (list, tuple))):
      #self.log_debug("  (list, tuple)")
      cnt = 0
      data = []
      for item in scheme:
        data.append(self._process_scheme(item))
        cnt += 1
      return data
    elif (isinstance(scheme, dict)):
      #self.log_debug("  (dict)")
      data = {}
      for k,v in scheme.items():
        data[k] = self._process_scheme(v)
      return data
    else:
      try:
        val = scheme()
        #self.log_debug("  (func) : {}".format(val))
        return val
      except TypeError:
        #self.log_debug("  (other) : {}".format(scheme))
        return str(scheme)
