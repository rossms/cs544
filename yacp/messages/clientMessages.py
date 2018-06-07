#!/usr/bin/python

# clientMessages.py
# Created 05/27/2018 at 11:19AM by rossms
# These are the messages. Separate classes keeps things nice and tidy.


class ZeroZeroOne:
    def __init__(self, username, password, hostname, clientalias):
        self.u = username
        self.p = password
        self.h = hostname
        self.c = clientalias

class ZeroZeroTwo:
    def __init__(self, username, password, clientalias, updateflag, updatetext):
        self.u = username
        self.p = password
        self.c = clientalias
        self.f = updateflag
        self.t = updatetext

class ZeroZeroThree:
    def __init__(self, username, password, clientalias):
        self.u = username
        self.p = password
        self.c = clientalias

class ZeroZeroFour:
    def __init__(self, sender, recipient, text):
        self.s = sender
        self.r = recipient
        self.t = text

class ZeroZeroFive:
    def __init__(self, username, clientalias):
        self.u = username
        self.c = clientalias

class FiveZeroOne:
    def __init__(self, status, text):
        self.s = status
        self.t = text

class FiveZeroThree:
    def __init__(self, status, text, message):
        self.s = status
        self.t = text
        self.m = message

class FiveZeroFour:
    def __init__(self, status, text):
        self.s = status
        self.t = text

class NineZeroOne:
    def __init__(self, text):
        self.t = text

class NineZeroTwo:
    def __init__(self, action, text):
        self.a = action
        self.t = text
