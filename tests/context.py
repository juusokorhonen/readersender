#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unit tests using the pytest framework.

@file           context.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "src")))
import readersender    # noqa: E402


__all__ = [
    'readersender'
]
