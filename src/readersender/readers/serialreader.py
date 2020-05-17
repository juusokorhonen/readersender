#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Simple reader for serial/uart.

@file           serialreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import serial
import serial.tools.list_ports
from ..reader import Reader
from ..helpers import (only_connected, only_disconnected)


class SerialReader(Reader):
    DEFAULT_SERIAL_CONFIG = dict(
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0,
        xonxoff=False,
        rtscts=False,
        write_timeout=1.0,
        dsrdtr=False,
        inter_byte_timeout=None
    )
    READ_MODES = ['line', 'bytes', 'until']

    def __init__(self, port, serial_config={}, read_command=None,
                 read_mode='line', max_bytes=1, end_mark='\n',
                 encoding='utf-8', timeout=None,
                 **kwargs):
        """Initializes a new SerialReader object.
        """
        super().__init__(**kwargs)
        # Any custom initialization goes here or to subclasses

        self._serial_config = self.DEFAULT_SERIAL_CONFIG.copy()
        self._serial_config.update(serial_config)
        self._serial_config['port'] = port
        if timeout is not None:
            self._serial_config['timeout'] = float(timeout)
            self._serial_config['write_timeout'] = float(timeout)

        # NOTE: Opens connection on creation
        self._serial = serial.Serial(**self._serial_config)

        self._read_command = str(read_command) if read_command is not None else None
        self._encoding = encoding

        if read_mode not in self.READ_MODES:
            raise AttributeError("Read mode unknown '{}'.".format(read_mode))
        self._read_mode = read_mode

        self._max_bytes = max(1, int(max_bytes))

        self._end_mark = str(end_mark)

    @only_connected(action='warn')
    def read(self, flush=False):
        """Reads data from the reader.

        Parameters
        ----------
        flush : boolean
            If True, dismiss everything in input buffer before running this command

        Returns
        -------
        str
            Data read from the serial.

        Notes
        -----
        Returns None, if a read timeout occurs.
        """
        if flush:
            self.serial.reset_input_buffer()
        if self.read_command is not None:
            try:
                self.serial.write(self.read_command.encode(self.encoding))
            except serial.SerialTimeoutException:
                pass
        try:
            return self.serial.readline().decode(self.encoding)\
                   if self.read_mode == "line"\
                   else self.serial.read(self.max_bytes).decode(self.encoding)\
                   if self.read_mode == 'bytes'\
                   else self.serial.read_until(self.end_mark).decode(self.encoding)
        except serial.SerialTimeoutException:
            return None

    @staticmethod
    def available_ports():
        return list(str(x) for x in serial.tools.list_ports.comports())

    @only_disconnected(action='pass')
    def connect(self):
        """Connects to serial instance.
        """
        self.serial.open()

    @only_connected(action='pass')
    def disconnect(self):
        """Disconnects from serial instance.
        """
        self.serial.close()

    @property
    def connected(self):
        """Returns if serial is connected.
        """
        return self.serial.is_open

    @property
    def serial(self):
        """Returns the internal serial instance.
        """
        return self._serial

    @property
    def read_command(self):
        """Read command is sent over serial to trigger a data read.
        """
        return self._read_command

    @read_command.setter
    def read_command(self, read_command):
        """Sets the read command.
        """
        self._read_command = str(read_command) if read_command is not None else None

    @property
    def encoding(self):
        """Encoding to use for converting unicode strings to byte strings.
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """Sets the encoding to use for converting unicode strings to byte strings.
        """
        self._encoding = encoding

    @property
    def read_mode(self):
        """Read mode in use.
        Currently, either 'line' to read a single line, or 'bytes' to read up to 'max_bytes'.
        """
        return self._read_mode

    @read_mode.setter
    def read_mode(self, value):
        """Sets the read mode.
        """
        if value not in self.READ_MODES:
            raise AttributeError("Read mode unknown '{}'.".format(value))
        self._read_mode = value

    @property
    def max_bytes(self):
        """Maximum bytes to read in 'bytes' read mode.
        """
        return self._max_bytes

    @max_bytes.setter
    def max_bytes(self, value):
        """Sets maximum bytes to read in 'bytes' read mode.
        """
        self._max_bytes = max(1, int(value))

    @property
    def end_mark(self):
        """The value to read until.
        """
        return self._end_mark

    @end_mark.setter
    def end_mark(self, value):
        """Set the end mark value for read mode 'until'.
        """
        self._end_mark = str(value)
