#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
MQTTSender class.

@file           mqttsender.py
@author:        Juuso Korhonen (jk.lic at_server fw.turqoosi.net)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import paho.mqtt.client as mqtt

from senders import senders

class MQTTSender(Sender):
	def __init__(self):      
    """      
    Initializes a new MQTTSender object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super(Sender, self).__init__()
    # Any custom initialization goes here or to subclasses
    self.config = {
    	'host': 'localhost',
    	'port': 1883,
    	'keepalive': 60,
    	'bind_adderss': ''
    }
    self.connected = False
    self.client = mqtt.Client()

  def connect(self):
  	"""
  	Connects to the mqtt instance.
  	"""
  	if not self.client:
  		raise RuntimeError("Client is not initialized")

  	if not self.connected:
	  	self.client.on_connect = self.on_connect
	  	client.connect(self.config.get('host'), self.config.get('port'), self.config.get('keepalive'), self.config.get('bind_adderss'))

  def on_connect(self):
  	"""
  	This method is called when successfully connected to client.
  	"""
  	self.connected = True

  def on_disconnect(self):
  	self.connected = False

  def send(self, data):
    """
    Data to be sent.
    \param[in]    data    - Energy data to send
    \remarks      Implement this in subclass. 
    """
    return