#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           test_mqttsender.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import pytest
import os
import pty
import string
try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError:
    print("Cannot test mqtt functionality without 'paho.mqtt'. Skipping tests.")
    mqtt = None


@pytest.mark.skipif(mqtt is None, reason="Cannot test without 'paho.mqtt' module.")
def test_mqttsender():
    """Tests importing and basic functionality of mqttsender.
    """
    from readersender.senders import MqttSender

    assert MqttSender() is not None

    
