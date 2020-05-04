#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging


def only_connected(action='pass'):
    """A decorator that allows the function to fail if connection is not available.
    @param method - Method to decorate
    @param action : str/function - Action to take, if condition is not met (default: pass).
        Can be a string 'pass', 'warn', or 'raise', or a function
        that receives the function as a parameter.
    """
    def fail_action():
        if action == 'pass':
            return lambda *args, **kwargs: None
        if action == 'warn':
            return lambda *args, **kwargs:\
                args[0].log("Failed assertion: not connected.", logging.WARN)
        if action == 'raise':
            return lambda *args, **kwargs: (_ for _ in ()).\
                throw(RuntimeError("Failed assertion: not connected."))
        return lambda *args, **kwargs: action(*args, **kwargs)
    fail_action = fail_action()

    def wrapped_method(method):
        def wrapper(*args, **kwargs):
            if not args[0].connected:
                fail_action(*args, **kwargs)
                return
            else:
                return method(*args, **kwargs)
        return wrapper
    return wrapped_method


def only_disconnected(action='pass'):
    """A decorator that allows the function to fail is connection is already made.
    @param method - Method to decorate
    @param action : str/function - Action to take, if condition is not met (default: pass).
        Can be a string 'pass', 'warn', or 'raise', or a function
        that receives the function as a parameter.
    """
    def fail_action():
        if action == 'pass':
            return lambda *args, **kwargs: None
        if action == 'warn':
            return lambda *args, **kwargs:\
                args[0].log("Failed assertion: not disconnected.", logging.WARN)
        if action == 'raise':
            return lambda *args, **kwargs: (_ for _ in ()).\
                throw(RuntimeError("Failed assertion: not disconnected."))
        return lambda *args, **kwargs: action(*args, **kwargs)
    fail_action = fail_action()

    def wrapped_method(method):
        def wrapper(*args, **kwargs):
            if args[0].connected:
                fail_action(*args, **kwargs)
                return
            else:
                return method(*args, **kwargs)
        return wrapper
    return wrapped_method
