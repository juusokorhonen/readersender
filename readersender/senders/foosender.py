#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo sender for testing.

@file           foosender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
from ..sender import Sender


class FooSender(Sender):
  """
  A foo sender class that does nothing.
  @version 1.0
  """
  def connect(self):
    self.log("Connecting to foo", logging.INFO)
    return True


  def disconnect(self):
    self.log("Disconnecting from foo", logging.INFO)


  def send(self, data):
    self.log("Sending (not really) data: {}".format(data), logging.INFO)
