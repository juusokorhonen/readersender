#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Console reader

@file           read_scripts.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import os
import sys
import time
import signal
import argparse
import traceback
import json
import logging
import logging.handlers
import importlib
sys.path.insert(0, os.path.abspath('../readersender/'))


def read_from_reader(readername,
                     readerargs=None,
                     logger=None, loglevel=logging.INFO):
    """Reads a single value from reader.
    """
    # Set up reader
    logger.debug("Initializing a reader")
    rmodname = readername.lower() + "reader"
    try:
        readermodule = importlib.import_module("." + rmodname, package='readersender.readers')
    except ImportError as e:
        logger.error("Could not import module: {}. Message: '{}'.".format(rmodname, e))
        sys.exit(1)

    rclassname = readername[0].upper() + readername[1:] + "Reader"
    try:
        Reader = getattr(readermodule, rclassname)
        reader = Reader(logger=logger, loglevel=loglevel, **readerargs.get('init'))
    except Exception as e:
        logger.error("Could not create reader class: {}. Message: '{}'.".format(rclassname, e))
        sys.exit(1)

    # Try connection to reader
    logger.debug("Connecting to reader")
    try:
        reader.connect()
    except Exception as e:
        logger.error("Connection to reader failed. Message: '{}'.".format(e))
        sys.exit(1)

    def read_data(**kwargs):
        # Connect to the reader
        if not reader.connected:
            reader.connect()
        data = reader.read(**kwargs)
        reader.disconnect()
        return data

    try:
        start_time = time.time()
        # Get data
        data = read_data(**readerargs.get('read'))
        runtime = time.time() - start_time
        logger.debug("Read data in {:.3f} seconds.".format(runtime))
    except Exception as e:
        # Catch all exceptions and carry on
        logger.error("Caught exception: {}".format(e))
        logger.debug(traceback.format_exc())
        return None

    return data


def read_value():
    """Sets up a reader and prints a single value.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('reader', help="reader class to use")
    parser.add_argument('--debug', help="run in debug mode (default: no)",
                        action='store_true')
    parser.add_argument('--reader_init_args',
                        help="Additional key-value arguments for reader initialization",
                        type=json.loads)
    parser.add_argument('--read_args',
                        help="Additional key-value arguments for read command",
                        type=json.loads)
    args = parser.parse_args()

    # Some application-specifig setup code
    reader = args.reader
    readerargs = {
        'init': {},
        'read': {},
    }
    readerargs['init'].update(args.reader_init_args or {})
    readerargs['read'].update(args.read_args or {})

    # Set up logger
    print("Setting up logging module")

    logname = 'read_value'
    loglevel = logging.INFO
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)
    handler = logging.StreamHandler()

    # Format for the logs
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if (args.debug):
        logger.info("Enabled debug mode")
        loglevel = logging.DEBUG
        logger.setLevel(loglevel)

    def exit_gracefully(signal, frame):
        """
        Exits from the program gracefully.
        """
        logger.info("Exiting...")
        sys.exit(0)

    # Make a signal catcher
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    logger.debug("Starting to read value")
    data = read_from_reader(reader,
                            readerargs,
                            logger=logger, loglevel=loglevel)
    logger.dedug("Read finished.")
    sys.stdout.write(data)
    sys.stdout.flush()
    sys.exit(0)


if __name__ == '__main__':
    read_value()
