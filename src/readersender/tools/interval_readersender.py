#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reader-sender model test app.

@file           app.py
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


def main_loop(readername, sendername,
              readerargs=None, senderargs=None,
              run_interval=10, logger=None, loglevel=logging.INFO):
    """Runs a reader/sender program at set intervals.
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

    # Set up sender
    logger.debug("Initializing a sender")
    smodname = sendername.lower() + "sender"
    try:
        sendermodule = importlib.import_module("." + smodname, 'readersender.senders')
    except ImportError as e:
        logger.error("Could not import module: {}. Message: '{}'.".format(smodname, e))
        sys.exit(1)

    sclassname = sendername[0].upper() + sendername[1:] + "Sender"
    try:
        Sender = getattr(sendermodule, sclassname)
        sender = Sender(logger=logger, loglevel=loglevel, **senderargs.get('init'))
    except Exception as e:
        logger.error("Could not create sender class: {}. Message: '{}'.".format(sclassname, e))
        sys.exit(1)

    logger.debug("Testing connection to sender")
    try:
        sender.connect()
    except RuntimeError as e:
        logger.error("Connection to sender failed. Message: '{}'.".format(e))
        sys.exit(1)

    # Auxillary functions
    def read_data(disconnect_after_read=True, **kwargs):
        # Connect to the reader
        if not reader.connected:
            reader.connect()

        # Read data
        data = reader.read(**kwargs)

        # Disconnect from reader
        if (disconnect_after_read):
            reader.disconnect()

        return data

    def send_data(data, disconnect_after_send=True, **kwargs):
        # Connect to the sender
        if not sender.connected:
            sender.connect()

        # Send data
        sender.send(data, **kwargs)   # NOTE: Dismisses result

        # Disconnect
        if (disconnect_after_send):
            sender.disconnect()

    # Run the loop
    try:
        while True:
            runtime = time.time()
            # Get data
            data = read_data(disconnect_after_read=readerargs.get('disconnect_after_read'),
                             **readerargs.get('read'))

            # Send data
            send_data(data, disconnect_after_send=senderargs.get('disconnect_after_send', True),
                      **senderargs.get('send'))
            # Log output to debug
            logger.debug("Data sent: {}".format(data))

            # Make a delay
            delay = run_interval - (time.time() - runtime)
            if (delay > 0):
                logger.debug("Waiting for {:.2f} s.".format(delay))
                time.sleep(delay)

    except Exception as e:
        # Catch all exceptions and carry on
        logger.error("Caught exception: {}".format(e))
        logger.debug(traceback.format_exc())


def interval_readersender():
    """Sets up a reader and a sender that pass data each interval.
    @notes Reads command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('reader', help="reader class to use")
    parser.add_argument('sender', help="sender class to use")
    parser.add_argument('interval', help="run interval in seconds", type=int)
    parser.add_argument('--debug', help="run in debug mode (default: no)",
                        action='store_true')
    parser.add_argument('--stdout', help="direct logs to stdout (default: no)",
                        action='store_true')
    parser.add_argument('--reader_init_args',
                        help="Additional key-value arguments for reader initialization",
                        type=json.loads)
    parser.add_argument('--read_args',
                        help="Additional key-value arguments for read command",
                        type=json.loads)
    parser.add_argument('--sender_init_args',
                        help="Additional key-value arguments for sender initialization",
                        type=json.loads)
    parser.add_argument('--send_args',
                        help="Additional key-value arguments for send command",
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
    sender = args.sender
    senderargs = {
        'init': {},
        'send': {},
        'disconnect_after_send': False,
    }
    senderargs['init'].update(args.sender_init_args or {})
    senderargs['send'].update(args.send_args or {})

    # Set up logger
    print("Setting up logging module")

    logname = 'readersender'
    loglevel = logging.INFO
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)

    if (not args.stdout):
        logfile = 'readersender.log'
        # Set up the handler to rotate logs every midnight and keep 3 copies
        handler = logging.handlers.TimedRotatingFileHandler(logfile, when="midnight",
                                                            backupCount=3)
    else:
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

    # Run the main loop
    restart_delay = 60
    max_restarts = 20
    restarts = 0
    while True:
        logger.info("Starting main loop")
        main_loop(reader, sender,
                  readerargs, senderargs,
                  run_interval=args.interval,
                  logger=logger, loglevel=loglevel)

        # Main loop exited
        restarts += 1
        if restarts > max_restarts:
            logger.error("Maximum number of restarts ({}) reached. Exiting."
                         .format(max_restarts))
            sys.exit(1)

        logger.info("Restarting main thread in {}s.".format(restart_delay))
        time.sleep(restart_delay)

    logger.error("Anomalously exiting main thread.")
    sys.exit(1)


if __name__ == '__main__':
    interval_readersender()
