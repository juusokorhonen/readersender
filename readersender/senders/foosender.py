#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Foo sender for testing.

@file           foosender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import abc

import senders

class FooSender(senders.Sender):
  """
  A foo sender class that does nothing.
  @version 1.0
  """

  def connect(self):
    self.log_debug("Connecting to foo")
    return True

  def disconnect(self):
    self.log_debug("Disconnecting from foo")

  def send(self, data):
    self.log_debug("Sending (not really) data: {}".format(data))
