#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           test_basic.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import sys


# Test definitions
def test_python_version():
    """Tests for proper python version.
    """
    assert sys.version_info.major == 3


def test_imports():
    """Tests importing the modules.
    """
    from .context import readersender   # noqa: F401


def test_readersender():
    """Tests readersender creation.
    """
    from .context import readersender

    assert isinstance(readersender.ReaderSender(), object)
    assert isinstance(readersender.Reader(), readersender.ReaderSender)
    assert isinstance(readersender.Sender(), readersender.ReaderSender)


def test_readersender_context():
    """Tests context functionality of readersender.
    """
    from .context import readersender

    with readersender.ReaderSender() as rs:
        assert rs.connected
        rs.disconnect()
        assert not rs.connected


def test_fooreader():
    """Tests the FooReader class.
    """
    from .context import readersender

    fr = readersender.readers.FooReader()

    fr.connect()
    fr.read()
    fr.disconnect()


def test_foosender():
    """Tests the FooSender class.
    """
    from .context import readersender

    fs = readersender.senders.FooSender()

    fs.connect()
    fs.send("testdata")
    fs.disconnect()


def test_randomreader():
    """Tests the RandomReader class.
    """
    from .context import readersender

    rr = readersender.readers.RandomReader()

    rr.connect()
    rr.read()
    rr.disconnect()
