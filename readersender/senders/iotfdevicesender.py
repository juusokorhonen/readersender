#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
IOTFDeviceSender class.

@file           iotfdevicesender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)

import logging
import os.path
import json
import ibmiotf.device

import senders

class IOTFDeviceSender(senders.Sender):
  """
  IOTFDeficeSender emulates an Watson IoT Platform device.
  """
  def __init__(self, config=None, configfile='iotf_device_config.txt', logger=None, loglevel=logging.INFO):      
    """      
    Initializes a new MQTTSender object. After
    initialization, you can set eg. debug_mode, silent_mode, and log_format
    parameter.   
    """         
    super(IOTFDeviceSender, self).__init__(logger=logger, loglevel=loglevel)

    # Any custom initialization goes here or to subclasses
    self.config = {
      'org': 'PLEASE SET <org_id>',
      'type': 'PLEASE SET <device_type>',
      'id': 'PLEASE SET <device_id>',
      'auth-method': 'token',
      'auth-token': 'PLEASE SET <auth_token>'
    }
    
    if (configfile is not None):
      try:
        self.config.update(ibmiotf.device.ParseConfigFile(configfile))
      except ibmiotf.ConnectionException as e:
        self.log_error("Could not load IBM IOTF config file")
        self.log_debug("{}".format(e))
      except Exception as e:
        self.log_error("Could not parse IBM IOTF config")
        self.log_debug("{}".format(e))

    if (config is not None):
      self.config.update(config)

    self.connected = False
    self.client = None

  @property
  def device_id(self):
    return self.config.get('id')

  @property
  def device_type(self):
      return self.config.get('type')
  
  def connect(self):
    """
    Connect to IBM IOTF.
    """
    if not self.client:
      self.connected = False
      try:
        self.log_debug('Initializing an IBM IOTF client with config :')
        for k,v in self.config.items():
          self.log_debug('  {}: {}'.format(k,v))
        self.client = ibmiotf.device.Client(self.config)
      except ibmiotf.ConnectionException as e:
        raise RuntimeError("Could not connect to IBM IOTF: {}".format(e))
      # Set logger to client
      if (self.logger is not None):
        self.client.logger = self.logger
      if (self.loglevel is not None):
        self.client.logger.setLevel(self.loglevel)

    if not self.connected:
      self.log_debug('Connecting to IBM IOTF')
      try:
        self.client.connect()
      except ibmiotf.ConnectionException as e:
        self.log_error("Could not connect to IBM IOTF")
        self.log_debug("{}".format(e))
        raise RuntimeError("Could not connect to IBM IOTF")
      else:
        self.connected = True

  def disconnect(self):
    """
    Disconnect from IBM IOTF.
    """
    self.log_debug('Disconnecting from IBM IOTF')
    self.client.disconnect()
    self.connected = False

  def send(self, payload, eventid='data', fmt='json', qos=0, on_publish=None):
    """
    Publish a device event.
    @param    payload   - Payload to be sent. Can be either a dict or anything else that can be converted to string. 
                          Payload will be encapsulated in {'d': payload} unless it is already done.

    """
    if (not self.client) or (not self.connected):
      raise RuntimeError("IBM IOTF client is not connected.")

    message = self._format_message(payload)

    self.log_debug("Publishing to topic: iot-2/evt/{eid}/fmt/{fmt}".format(eid=eventid, fmt=fmt))
    self.log_debug("  with a message: {}".format(message))
    self.client.publishEvent(eventid, fmt, message, qos=qos, on_publish=on_publish)

  @property
  def logger(self):
    return self._logger

  @logger.setter
  def logger(self, logger):
    self._logger = logger
    if (self.client is not None):
      self.client.logger = logger

  @property
  def loglevel(self):
      return self._loglevel

  @loglevel.setter
  def loglevel(self, loglevel):
    self._loglevel = loglevel
    if (self.client is not None):
      self.client.logger.loglevel = loglevel

  def _format_message(self, message):
    """
    Internal function that formats data as requested.
    """
    if not isinstance(message, dict):
      message = {'d': message}

    else:
      if 'd' not in message:
        message = {'d': message}

    return message

  def _unicode_to_bytes(self, data):
    if (isinstance(data, (list, tuple))):
      ndata = []
      for item in data:
        ndata.append(self._unicode_to_bytes(item))
      return ndata
    elif (isinstance(data, dict)):
      ndata = {}
      for k,v in data.items():
        ndata[bytes(k)] = self._unicode_to_bytes(v)
      return ndata
    else:
      return bytes(data)
