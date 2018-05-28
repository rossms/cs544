
class ZeroZeroOne:
    def __init__(self, username, password, hostname, clientalias):
        self.u = username
        self.p = password
        self.h = hostname
        self.c = clientalias

class ZeroZeroFive:
    def __init__(self, username, clientalias):
        self.u = username
        self.c = clientalias

class ZeroZeroFour:
    def __init__(self, sender, recipient, text):
        self.s = sender
        self.r = recipient
        self.t = text