#!/usr/bin/python           # This is client.py file

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from messages.clientMessages import *
from threading import *

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
r = s.recv(1024).decode()
print r

keepopen = 1

def run(alive):
    while alive:

        print "Choose option: Register(r), update(u), send(s), close(x), get(g)"
        action = raw_input()

        if action == "r":
            print "Enter username"
            username = raw_input()
            t = ZeroZeroOne(username,"testpass","testhost","testalias")
            buffer = "1.0"+"001"+t.u +"|"+ t.p +"|"+ t.h +"|"+ t.c +"|"+ "\\\\"
            s.send(buffer)
            r = s.recv(1024).decode()
            print r

        if action == "u":
            t = ZeroZeroOne("testuser","testpass","testhost","testalias")
            buffer = "1.0"+"002"+t.u +"|"+ t.p +"|"+ t.h +"|"+ t.c +"|"+ "\\\\"
            s.send(buffer)
            r = s.recv(1024).decode()
            print r

        if action == "s":
            t = ZeroZeroFour("testuser1","testuser2","hey there")
            buffer = "1.0"+"004"+t.s+"|"+t.r+"|"+t.t+"|"+ "\\\\"
            s.send(buffer)
            r = s.recv(1024).decode()
            print r

        if action == "x":
            t = ZeroZeroFive("testuser","testalias")
            buffer = "1.0"+"005"+t.u+"|"+t.c+"|"+ "\\\\"
            s.send(buffer)
            break

        if action =="g":
            r = s.recv(1024).decode()
            print r



run(keepopen)


#print action

#print(r[:1])


#s.close                     # Close the socket when done





# TODO: All client to server messages

# TODO : keep client connection open

# TODO : how to handle user actions through CL?

# TODO: : DFA

