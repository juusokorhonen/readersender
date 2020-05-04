#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           test_serialreader.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import pytest
import os
import pty
import string
try:
    import serial
except ModuleNotFoundError:
    print("Cannot test serial functionality without 'pyserial'. Skipping tests.")
    serial = None


@pytest.fixture
def fake_serial_ports():
    """Creates a fake pair of tty's

    Returns
    -------
    tuple(master_pty, slave_serial)
        PTY name for master.
        TTU name for slave.
    """
    master, slave = pty.openpty()
    return (master, os.ttyname(slave))


@pytest.mark.skipif(serial is None, reason="Cannot test without 'serial' module.")
@pytest.mark.skipif(pty is None, reason="Cannot test without 'pty' module (available on " +
                    "unix-like platforms).")
def test_serialreader(fake_serial_ports):
    """Tests importing and basic functionality of serialreader.
    """
    from readersender.readers import SerialReader

    master_pty, slave_tty = fake_serial_ports

    assert master_pty is not None
    assert slave_tty is not None

    available_ports = SerialReader.available_ports()
    assert available_ports is not None
    assert isinstance(available_ports, list)
    assert len(available_ports) > 0

    sr = SerialReader(port=slave_tty)
    assert sr.connected
    sr.connect()
    assert sr.connected

    sr.serial.reset_input_buffer()
    assert sr.serial.in_waiting == 0

    with os.fdopen(master_pty, "wb") as fd:
        assert sr.encoding == 'utf-8'
        probe_msg = bytes("".join(string.ascii_letters + string.digits + string.punctuation),
                          encoding='utf-8')
        fd.write(probe_msg)
        fd.flush()

        assert sr.serial.in_waiting == len(probe_msg)
        assert sr.read() == probe_msg
        assert sr.serial.in_waiting == 0

        sr.disconnect()
        assert not sr.connected

        probe_msg = bytes("Sáhtán borrat lása, dat ii leat bávččas.",
                          encoding='cp1250')
        sr.encoding = 'cp1250'
        assert sr.encoding == 'cp1250'

        assert sr.read_command is None
        sr.read_command = 'p'
        assert sr.read_command == 'p'

        sr.connect()
        assert sr.serial.in_waiting == 0
        fd.write(probe_msg)
        fd.flush()
        assert sr.serial.in_waiting == len(probe_msg)

        assert len(sr.read(flush=True)) == 0

        fd.write(probe_msg)
        fd.flush()

        assert sr.read() == probe_msg
