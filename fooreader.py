#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo reader for testing.

@file           fooreader.py
@author:        Juuso Korhonen (jk.lic at_server fw.turqoosi.net)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import abc

import readers

class FooReader(readers.Reader):
  """
  A foo reader class that does nothing.
  @version 1.0
  """

  def connect(self):
    self.log_debug("Connecting to foo")
    return True

  def disconnect(self):
    self.log_debug("Disconnecting from foo")

  def read(self):
    data = "foo"
    self.log_debug("Reading (not really) data: {}".format(data))
    return data