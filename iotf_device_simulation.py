#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Send test MQTT packets interactively.

@file           iotf_device_simulation.py
Project:        Project Saimaa, 2016
Author:         Juuso Korhonen  / Espotel Oy, Espoo, FINLAND
"""
from __future__ import (absolute_import, division, unicode_literals, print_function)
import sys
import time
import datetime
import signal
import abc
import argparse
import traceback
import logging
import logging.handlers
import importlib
import json
import random
import uuid

import ibmiotf
import requests

from loggers import SimpleLogger
from readers import Reader
from senders import Sender

__version__ = "develop"
__date__ = "2016-04-05"

def wait_s(t):
  endtime = time.time() + t
  delay = 0.0005
  while True:
    remaining = endtime - time.time()
    if (remaining <= 0):
      return
    delay = min(delay * 2, remaining, .05)
    time.sleep(delay)

def pump_running():
  global p_running
  try:
    return p_running
  except NameError as e:
    p_running = False
    return p_running

class Pump(object):
  STATUS_RUNNING = 0
  STATUS_STOPPED = 1
  STATUS_STARTING = 2
  STATUS_STOPPING = 3
  STATUS_ERROR = 4
  STATUSES = [STATUS_RUNNING, STATUS_STOPPED, STATUS_STARTING, STATUS_STOPPING, STATUS_ERROR]

  def __init__(self):
    self.status = self.STATUS_STOPPED
    self.__deferTime = None
    self.__deferStatus = None

  @property
  def status(self):
    if (self.__deferTime is not None):
      if (time.time() > self.__deferTime):
        self._status = self.__deferStatus
        self.__deferTime = None
        self.__deferStatus = None
    return self._status

  @status.setter
  def status(self, val):
    if (val in self.STATUSES):
      self._status = val
      self.__deferTime = None
      self.__deferStatus = None

  def running(self):
    return (self.status == self.STATUS_RUNNING)

  def stopped(self):
    return (self.status == self.STATUS_STOPPED)

  def start(self):
    if (self._startAllowed()):
      self.status = self.STATUS_STARTING
      delay = random.choice([1,3,5,10,20])
      self.__deferStatusChange(self.STATUS_RUNNING, delay)
      return True
    return False

  def stop(self):
    if (self._stopAllowed()):
      self.status = self.STATUS_STOPPING
      delay = random.choice([1,3,5,10,20])
      self.__deferStatusChange(self.STATUS_STOPPED, delay)
      return True
    return False      

  def __deferStatusChange(self, status, delay):
    if (status in self.STATUSES and delay >= 0):
      self.__deferTime = time.time() + delay
      self.__deferStatus = status

  def _startAllowed(self):
    if (self.__deferTime is not None):
      return False
    return (self.status in [self.STATUS_STOPPED, self.STATUS_ERROR])

  def _stopAllowed(self):
    if (self.__deferTime is not None):
      return False
    return (self.status in [self.STATUS_RUNNING, self.STATUS_ERROR])   

def iotf_device_simulation():
  def print_menu(menu, level=0):
    print("Menu:")
    for k in sorted(menu.keys()):
      v = menu.get(k)
      if (isinstance(v, dict)):
        print_menu(v, level=level+1)
      else:
        print("\t"+(2*level)*" "+"{}\t{}".format(k,v))

  def wait_input(choices):
    while (True):
      try:
        i = raw_input('Selection: ')
      except:
        print("\nCaught exception. Exiting...")
        iotf.disconnect()
        iotf_app.disconnect()
        wait_s(5)
        raise RuntimeError()

      if (i in choices):
        return i

  def print_status(iotf_app, iotf_dev):
    if (iotf_app.connected):
      print("IOTF application is connected")
    else:
      print("IOTF application is not connected")

    if (iotf_dev.connected):
      print("IOTF Device is connected")
    else:
      print("IOTF Device is not connected")

  loglevel = logging.INFO
  applogger = logging.getLogger(__name__+"_app")
  devlogger = logging.getLogger(__name__+"_dev")
  applogger.setLevel(loglevel)
  devlogger.setLevel(loglevel)
  apphandler = logging.FileHandler('iotf_device_simulation_app.log')
  devhandler = logging.FileHandler('iotf_device_simulation_dev.log')
  #handler = logging.StreamHandler()
  #handler = logging.handlers.TimedRotatingFileHandler(logfile, when="midnight", backupCount=3)
  #logging.basicConfig(level=loglevel)
  formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
  apphandler.setFormatter(formatter)
  devhandler.setFormatter(formatter)
  applogger.addHandler(apphandler)
  devlogger.addHandler(devhandler)

  scheme = {
    'ts': lambda: datetime.datetime.utcnow().isoformat(),
    'd': {
      'temp': {
        'T1': lambda: round(random.normalvariate(25.0, 10.0), 2),
        'T2': lambda: round(random.normalvariate(30.0, 15.0), 2),
        'T3': lambda: round(random.normalvariate(35.0, 20.0), 2),
        'T4': lambda: round(random.normalvariate(40.0, 25.0), 2),
        'T5': lambda: round(random.normalvariate(45.0, 30.0), 2),
        'T6': lambda: round(random.normalvariate(50.0, 35.0), 2),
        'T7': lambda: round(random.normalvariate(55.0, 40.0), 2),
        'T8': lambda: round(random.normalvariate(60.0, 45.0), 2),
        'T9': lambda: round(random.normalvariate(65.0, 50.0), 2)
      },
      'ctrl': {
        'spd': lambda: round(random.uniform(0, 100), 0),
        'pwr': lambda: round(random.uniform(0, 1000), 0),
        'sts': 'ok',
      },
      'exch': {
        'pri': {
          'Tin': lambda: round(random.normalvariate(25.0, 10.0), 2),
          'Tout': lambda: round(random.normalvariate(25.0, 10.0), 2),
          'p': lambda: round(random.normalvariate(1013.0, 50.0), 1),
          'flow': lambda: round(random.uniform(0, 100), 0),
          'pwr': lambda: round(random.uniform(0, 1000), 1),
          'E': lambda: round(random.uniform(0, 10000), 1)
        },
        'sec': {
          'Tin': lambda: round(random.normalvariate(25.0, 10.0), 2),
          'Tout': lambda: round(random.normalvariate(25.0, 10.0), 2),
          'p': lambda: round(random.normalvariate(1013.0, 50.0), 1),
          'flow': lambda: round(random.uniform(0, 100), 0),
          'pwr': lambda: round(random.uniform(0, 1000), 1),
          'E': lambda: round(random.uniform(0, 10000), 1)
        },
        'sts': 'ok',
        'alarm': None,
      },
      'emeter': {
        'E': lambda: round(random.uniform(0, 10000), 1)
      }
    }
  }

  import randomreader
  rnd = randomreader.RandomReader(scheme=scheme, loglevel=loglevel)

  import iotfsender
  iotf_app = iotfsender.IOTFSender(logger=applogger, loglevel=loglevel)

  import iotfdevicesender
  iotf = iotfdevicesender.IOTFDeviceSender(logger=devlogger, loglevel=loglevel)

  def exit_gracefully(signal, frame):
    """
    Exits from the program gracefully.
    """
    print("Exiting...")
    sys.exit(0)

  # Make a signal catcher
  signal.signal(signal.SIGINT, exit_gracefully)
  signal.signal(signal.SIGTERM, exit_gracefully)  
  
  mainmenu = {
    'p': 'Print status',
    'ac': 'Connect application',
    'cd': 'Connect device',
  }
  appmenu = {
    'as': 'Application subscribe to events and commands',
    'ad': 'Disconnect application',
    'adt': 'Send test command to device',
    'aps': 'Send pump start',
    'app': 'Send pump stop',
    'api': 'Request pump status',
    'ar': 'Send reboot to device',
  }
  devmenu = {
    'dd': 'Disconnect device',
    'dsh': 'Send hello',
    'dst': 'Send test message',
    'ds': 'Device subscribe to commands',
    'dm': 'Device become managed',
    'dsa': 'Send alarm',
  }
  menu = {}
  menu.update(mainmenu)
  try:
    while True:
      print_menu(menu)
      selection = wait_input(menu.keys())

      if (selection == 'p'):
        print_status(iotf_app, iotf)
      
      elif (selection == 'ac'):
        print("Connecting IOTF application")
        iotf_app.connect()
        if not iotf_app.connected:
          print("Connection failed.")
          continue
        menu.update(appmenu)
        menu.pop('ac')

      elif (selection == 'ad'):
        print("Disconnecting application")
        iotf_app.disconnect()
        menu.pop('ad')
        menu.update(mainmenu)
        continue
      
      elif (selection == 'as'):
        print("Subscribing to device events and commands")

        def appEventCallback(event):
          applogger.info("Event: fmt={fmt}, event={event}, device={device}, data={data}".format(fmt=event.format, event=event.event, device=event.device, data=json.dumps(event.data)))

        def appStatusCallback(status):
          if (status.action == "Disconnect"):
            applogger.info("Disconnect: time={time}, device={device}, action={action}, reason={reason}".format(time=status.time.isoformat(), device=status.device, action=status.action, reason=status.reason))
          else:
            applogger.info("Status: time={time}, device={device}, action={action}".format(time=status.time.isoformat(), device=status.device, action=status.action))

        def appCommandCallback(cmd):
          applogger.info("Command: device={device}, command={command}".format(device=cmd.device, command=cmd.command))

        iotf_app.client.deviceEventCallback = appEventCallback
        iotf_app.client.deviceStatusCallback = appStatusCallback
        iotf_app.client.deviceCommandCallback = appCommandCallback
  
        iotf_app.client.subscribeToDeviceEvents(qos=0)
        iotf_app.client.subscribeToDeviceStatus()
        iotf_app.client.subscribeToDeviceCommands()


      elif (selection == 'cd'):
        print("Connecting IOTF device")
        iotf.connect()
        if not iotf.connected:
          print("Connection failed")
          continue
        pump = Pump()
        menu.update(devmenu)
        menu.pop('cd')

      elif (selection == 'dd'):
        print("Disconnecting IOTF device")
        iotf.disconnect()
        if not iotf.connected:
          for k in devmenu.keys():
            menu.pop(k)
          menu.update({'cd': mainmenu['cd']})

      elif (selection == 'dsh'):
        print("Sending 'hello' message")
        evt = 'hello'
        fmt = 'json'
        msg = {}
        iotf.send(msg, eventid=evt, fmt=fmt)

      elif (selection == 'dst'):
        print("Sending test data")
        data = rnd.read()
        evt = 'data'
        fmt = 'json'
        iotf.send(data, eventid=evt, fmt=fmt)

      elif (selection == 'dsa'):
        print("Sending heat exchanger alarm")
        data = rnd.read()
        evt = 'data'
        fmt = 'json'
        data['d']['exch']['alarm'] = "Test alarm"
        iotf.send(data, eventid=evt, fmt=fmt)

      elif (selection == 'ds'):
        print("Subscribing to commands")
        def deviceCommandCallback(cmd):
          devlogger.info("Command: command={command}, format={format}, data={data}".format(command=cmd.command, format=cmd.format, data=json.dumps(cmd.data)))

          if ('reqId' in cmd.data):
            payload = {'reqId': cmd.data.get('reqId'), 'd': {}}
          else:
            payload = {'d': {}}

          if (cmd.command == 'ping'):
            devlogger.info("Got ping, sending pong")
            payload['rc'] = 200
            payload['d']['msg'] = 'pong'
            iotf.send(payload, eventid='response')
          elif (cmd.command == 'reboot'):
            devlogger.info("Got reboot request. Simulating reboot.")
            payload['rc'] = 202 # 202 = accepted
            payload['d']['msg'] = 'reboot initiated'
            iotf.send(payload, eventid='response')
            wait_s(2)
            try:
              iotf.unmanage()
            except:
              pass
            wait_s(5)
            if ('u' in menu):
              iotf.manage()
            payload['rc'] = 200
            payload['d']['msg'] = 'reboot finished'
            iotf.send(payload, eventid='response')

          elif (cmd.command == 'pump'):
            devlogger.info("Got pump command.")
            d = cmd.data.get('d')

            if (d is None) or (d.get('target') != 'pump01'):
              payload['rc'] = 404
              payload['msg'] = 'target not found'
              iotf.send(payload, eventid='response')
            else:
              if (d.get('action') == 'status'):
                status = pump.status
                payload['rc'] = 200
                if (status == pump.STATUS_RUNNING):
                  payload['msg'] = 'running'
                elif (status == pump.STATUS_STOPPED):
                  payload['msg'] = 'stopped'
                elif (status == pump.STATUS_STARTING):
                  payload['msg'] = 'starting'
                elif (status == pump.STATUS_STOPPING):
                  payload['msg'] = 'stopping'
                elif (status == pump.STATUS_ERROR):
                  payload['msg'] = 'error'
                else:
                  payload['msg'] = 'unknown'
                iotf.send(payload, eventid='response')

              elif (d.get('action') == 'start'):
                if (pump.start()):
                  devlogger.info("Switching pump on")
                  payload['rc'] = 202
                  payload['msg'] = 'starting pump'

                  def __start_pump(): 
                    i = 0.0
                    interval = 1.0
                    finished_successfully = False
                    while (not finished_successfully) and (i < 10):
                      wait_s(interval)
                      if (pump.running()):
                        payload['rc'] = 200
                        payload['msg'] = 'pump started'
                        iotf.send(payload, eventid='response')
                        finished_successfully = True
                      i += interval
                    if (not finished_successfully):
                      payload['rc'] = 500
                      payload['msg'] = 'pump could not be started'
                      iotf.send(payload, eventid='response')
                    
                  iotf.send(payload, eventid='response', on_publish=__start_pump)

                else:
                  devlogger.info("Not starting pump")
                  payload['rc'] = 400
                  payload['msg'] = 'pump already started'
                  iotf.send(payload, eventid='response')
              elif (d.get('action') == 'stop'):
                if (pump.stop()):
                  devlogger.info("Switching pump off")
                  payload['rc'] = 202
                  payload['msg'] = 'stopping pump'

                  def __stop_pump():
                    i = 0.0
                    interval = 1.0
                    finished_successfully = False
                    while (not finished_successfully) and (i < 10):
                      wait_s(interval)
                      if (pump.stopped()):
                        payload['rc'] = 200
                        payload['msg'] = 'pump stopped'
                        iotf.send(payload, eventid='response')
                        finished_successfully = True
                      i += interval
                    if (not finished_successfully):
                      payload['rc'] = 500
                      payload['msg'] = 'pump could not be stopped'
                      iotf.send(payload, eventid='response')

                  iotf.send(payload, eventid='response', on_publish=__stop_pump)

                else:
                  devlogger.info("Not stopping pump")
                  payload['rc'] = 400
                  payload['msg'] = 'pump already stopped'
                  iotf.send(payload, eventid='response')
              else:
                devlogger.info("Unrecognized pump action")
                payload['rc'] = 404
                payload['msg'] = 'unrecognized action'
                iotf.send(payload, eventid='response')

          else:
            devlogger.info("Unrecognized command")
            payload['rc'] = 404
            payload['d']['msg'] = "unrecognized command"
            iotf.send(payload, eventid="response")


        iotf.client.commandCallback = deviceCommandCallback

      elif (selection == 'du'):
        print("Becoming an unmanaged device")
        iotf.client.unmanage()

        menu.pop('du')
        menu['dm'] = devmenu['dm']

      elif (selection == 'dm'):
        print("Becoming a managed device")
        def deviceActionCallback(reqid, action):
          devlogger.info("Action: reqId={reqid}, action={action}".format(reqid=reqid, action=action))

        if (not isinstance(iotf.client, ibmiotf.device.ManagedClient)):
          device_info = ibmiotf.device.DeviceInfo()
          device_info.description = "cRIO test device"
          device_info.fwVersion = None
          device_info.hwVersion = None
          device_info.model = None
          device_info.serialNumber = None

          iotf.client.disconnect()
          wait_s(1)
          
          iotf.client = ibmiotf.device.ManagedClient(iotf.config, logHandlers=[devhandler], deviceInfo=device_info)
          iotf.client.deviceActionCallback = deviceActionCallback
          iotf.client.connect()
        
        iotf.client.manage(3600, supportDeviceActions=True, supportFirmwareActions=False)

        menu.pop('dm')
        menu['du'] = "Become unmanaged"

      elif (selection == 'adt'):
        print("Sending a test command to device")
        device_type = iotf.device_type
        device_id = iotf.device_id
        msg = {'reqId': str(uuid.uuid1())}
        cmds = [('ping', {}), ('foo', {'d': {'msg': 'bar'}}), ('reboot', {})]
        cmd = random.choice(cmds)
        msg.update(cmd[1])
        iotf_app.client.publishCommand(device_type, device_id, cmd[0], "json", msg)


      elif (selection == 'aps' or selection == 'app' or selection == 'api'):
        print("Sending a pump start/stop to device")
        device_type = iotf.device_type
        device_id = iotf.device_id
        
        msg = {'reqId': str(uuid.uuid1()), 'd': {'target': 'pump01'}}
        if (selection == 'aps'):
          msg['d']['action'] = 'start'
        elif (selection == 'app'):
          msg['d']['action'] = 'stop'
        else:
          msg['d']['action'] = 'status'

        cmd = 'pump'
        iotf_app.client.publishCommand(device_type, device_id, cmd, "json", msg)

      elif (selection == 'ar'):
        print("Sending a reboot action to managed device")
        device_type = iotf.device_type
        device_id = iotf.device_id
        #raise NotImplementedError("Functionality not implemented") 
        # TODO: Continue from here
        org = iotf_app.config.get('org')
        user = iotf_app.config.get('auth-key')
        password = iotf_app.config.get('auth-token')
        api_url = "https://{orgid}.internetofthings.ibmcloud.com/api/v0002/".format(orgid=org)
        endpoint = "mgmt/requests"
        payload = {
          'action': "device/reboot",
          'parameters': [],
          'devices': [
            {
              'typeId': 'crio-data',
              'deviceId': 'crio-test'
            }
          ]
        }
        r = requests.post(api_url+endpoint, json=payload, auth=(user, password))
        if (r.status_code == 202):
          applogger.info("Device reboot actions sent for processing")
        else:
          print("Failed to send reboot command. HTTP status code: {}".format(r.status_code))
          print(r.text)

  except Exception as e:
    print("Caught unexpected exception: {}".format(e))
    if iotf is not None and iotf.connected:
      iotf.disconnect()
    if iotf_app is not None and iotf_app.connected:
      iotf_app.disconnect()
    traceback.print_exc()
    sys.exit(1)


if __name__ == '__main__':
  iotf_device_simulation()
