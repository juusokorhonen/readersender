#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           test_module.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import sys
import pytest


# Test definitions
def test_python_version():
    """Tests for proper python version.
    """
    assert sys.version_info.major == 3
    

def test_readersender_import():
	"""Tests importing the readersender module.
	"""
	from .context import readersender
	

def test_readersender():
	"""Creates a readersender.
	"""
	from .context import readersender

	with pytest.raises(TypeError):
		readersender.ReaderSender()   # NOTE: Abstract class

	with pytest.raises(TypeError):
		readersender.Reader()

	with pytest.raises(TypeError):
		readersender.Sender()


def test_fooreader():
	"""Tests the FooReader class.
	"""
	from .context import readersender

	fr = readersender.FooReader()