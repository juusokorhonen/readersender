#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           run_tests.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import sys


# Test definitions
def test_python_version():
    """Tests for proper python version.
    """
    assert sys.version_info.major == 3
    

