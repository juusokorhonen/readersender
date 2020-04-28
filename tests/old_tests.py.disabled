#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Run some tests to see that everything is working.

@file           run_tests.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""

import sys
import time
import signal
import abc
import argparse
import traceback
import logging
import logging.handlers
import importlib
import json

from loggers import SimpleLogger
from readers import Reader
from senders import Sender

# ---------------------------------------------------------------------------------#


def run_tests(readername, sendername, loglevel=logging.INFO):
  """
  Runs a test sequence.
  """
  logging.basicConfig(level=loglevel)
  logger = logging.getLogger(__name__)
  logger.setLevel(loglevel)
  
  logger.info("Initializing a reader")
  rmodname = readername.lower() + "reader"
  try:
    readermodule = importlib.import_module(rmodname)
  except ImportError as e:
    logger.error("Could not import module: {}".format(rmodname))
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  rclassname = readername[0].upper() + readername[1:] + "Reader"
  try:
    Reader = getattr(readermodule, rclassname)
    reader = Reader(logger=logger, loglevel=loglevel)
  except AttributeError as e:
    logger.error("Could not create reader class: {}".format(rclassname))
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Connecting to reader")
  try:
    reader.connect()
  except RuntimeError as e:
    logger.error("Connection to reader failed")
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Reading data from reader")
  try:
    data = reader.read()
  except RuntimeError as e:
    logger.error("Reading data failed")
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Disconnecting reader")
  reader.disconnect()



  logger.info("Initializing a sender")
  smodname = sendername.lower() + "sender"
  try:
    sendermodule = importlib.import_module(smodname)
  except ImportError as e:
    logger.error("Could not import module: {}".format(smodname))
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  sclassname = sendername[0].upper() + sendername[1:] + "Sender"
  try:
    Sender = getattr(sendermodule, sclassname)
    sender = Sender(logger=logger, loglevel=loglevel)
  except AttributeError as e:
    logger.error("Could not create sender class: {}".format(sclassname))
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Connecting to sender")
  try:
    sender.connect()
  except RuntimeError as e:
    logger.error("Connection to sender failed")
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Sending data to sender")
  try:
    sender.send(data)
  except RuntimeError as e:
    logger.error("Sending data failed")
    logger.exception("Exception : {}".format(e))
    sys.exit(1)

  logger.info("Disconnecting sender")
  sender.disconnect()



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('reader', help="reader class to use")
  parser.add_argument('sender', help="sender class to use")
  parser.add_argument('--debug', help="run in debug mode (default: no)", action='store_true')
  args = parser.parse_args()

  if (args.debug):
    print("[INFO] Enabled debug mode")
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

  run_tests(args.reader, args.sender, loglevel=loglevel)
