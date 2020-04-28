#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo reader for testing.

@file           fooreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
from ..reader import Reader

class FooReader(Reader):
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
