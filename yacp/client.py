#!/usr/bin/python           # This is client.py file

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from messages.zerozeroone import ZeroZeroOne
#from threading import *

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
r = s.recv(1024).decode()
print r
print(r[:1])

t = ZeroZeroOne("testuser","testpass","testhost","testalias")
buffer = "1.0"+"001"+t.u + t.p + t.h + t.c + "\\\\"
s.send(buffer)
#s.close                     # Close the socket when done


# class client(Thread):
#     def __init__(self, socket, address):
#         Thread.__init__(self)
#         self.sock = socket
#         self.addr = address
#         self.start()
#
#     def run(self):
#         while 1:
#             print('Client sent:', self.sock.recv(1024).decode())
#             self.sock.send(b'Oi you sent something to me')


# TODO: All client to server messages

# TODO : keep client connection open

# TODO : input from user

# TODO : how to handle user actions through CL?

