#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
MQTTSender class.

@file           mqttsender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError:
    import warnings
    warnings.warn("'paho.mqtt.client' not found. MQTT functionality disabled.",
                  ImportWarning)
    mqtt = None
from ..sender import Sender
from ..helpers import (only_connected, only_disconnected)


if mqtt is not None:
    class MqttSender(Sender):
        MQTT_DEFAULT_CONFIG = {
            'host': 'localhost',
            'port': 1883,
            'keepalive': 60,
            'bind_address': '',
            'sync': False
        }

        def __init__(self, config=None, *args, **kwargs):
            """Initializes a new MQTTSender.
            """
            super().__init__(*args, **kwargs)
            # Any custom initialization goes here or to subclasses
            self.config = self.MQTT_DEFAULT_CONFIG.copy()
            if config is not None:
                self.config.update(config)
            self.connected = False
            self.client = mqtt.Client()

        @only_disconnected()
        def connect(self):
            """Connects to the MQTT instance.
            """
            if not self.client:
                raise RuntimeError("Client is not initialized")

            try:
                self.client.on_connect = self.on_connect
                conn_fun = self.client.connect if self.config.sync \
                    else self.client.connect_async
                conn_fun(
                    self.config.get('host'),
                    self.config.get('port'),
                    self.config.get('keepalive'),
                    self.config.get('bind_address'))
            except ConnectionRefusedError as e:
                raise RuntimeError("Connection refused: {}".format(e))

        def on_connect(self):
            """This method is called when successfully connected to client.
            """
            self.connected = True

        @only_connected()
        def disconnect(self):
            """Disconnects the MQTT instance.
            """
            if not self.client:
                raise RuntimeError("Client is not initialized")

            if self.connected:
                self.client.on_disconnect = self.on_disconnect
                self.client.disconnect()

        def on_disconnect(self):
            self.connected = False

        @only_connected(action='warn')
        def send(self, data):
            """
            Data to be sent.
            @param[in]    data - String-like data to send
            @remarks      Functionality not implemented
            """
            return
