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
        print(action)
        if action == 'pass':
            return lambda self, *args, **kwargs: None
        if action == 'warn':
            return lambda self, *args, **kwargs:\
                self.log("Already connected.", logging.WARN)
        if action == 'raise':
            return lambda self, *args, **kwargs: (_ for _ in ()).\
                throw(RuntimeError("Already connected."))
        return lambda self, *args, **kwargs: action(self, *args, **kwargs)
    fail_action = fail_action()

    def action(method):
        def wrapper(self, *args, **kwargs):
            if not self.connected:
                print(fail_action(self, *args, **kwargs))
            else:
                return method(self, *args, **kwargs)
        return wrapper
    return action


def only_disconnected(action='pass'):
    """A decorator that allows the function to fail is connection is already made.
    @param method - Method to decorate
    @param action : str/function - Action to take, if condition is not met (default: pass).
        Can be a string 'pass', 'warn', or 'raise', or a function
        that receives the function as a parameter.
    """
    def fail_action():
        if action == 'pass':
            return lambda self, *args, **kwargs: None
        if action == 'warn':
            return lambda self, *args, **kwargs:\
                self.log("Already connected.", logging.WARN)
        if action == 'raise':
            return lambda self, *args, **kwargs: (_ for _ in ()).\
                throw(RuntimeError("Already connected."))
        return lambda self, *args, **kwargs: action(self, *args, **kwargs)
    fail_action = fail_action()

    def action(method):
        def wrapper(self, *args, **kwargs):
            if self.connected:
                fail_action(self, *args, **kwargs)
            else:
                return method(self, *args, **kwargs)
        return wrapper
    return action
