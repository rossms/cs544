#!/usr/bin/python

# client.py
# Created 05/19/2018 at 2:47PM by rossms
# This is the client implementation

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import sys
from messages.clientMessages import *
from threading import *
from select import select

# global variables
version = "1.1"
keepOpen = 1

# functions

# do to the CLI implementation of this protocol, the client must handle both waiting for user input as well as
# checking to see if the server is sending any messages.


def raw_input_with_timeout():
    timeout = 2
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = sys.stdin.readline()
        return s.replace("\n", "")
    else:
        return "a"


def receive():
    try:
        received = s.recv(1024).decode()
        if received != "":
            body = received[6:-2]
            chunks = body.split("||")
            sender = chunks[0]
            chat = chunks[2]
            print sender + " sent you a message: " + chat
    except:
        pass

# once connected, the client will loop through the while alive. First it will always validate the current state
# of the client. Depending on the state, it can perform certain actions. These checks are the DFA gates. All
# messages get info from the user, and create an instance of the message class. This keeps things neat. It then
# builds a message buffer and sends the message to the server.


def run(alive):
    while alive:
        try:
            global currentState
            global currentUser
            global currentAlias
            global currentPassword

            if currentState == 1:
                print "Welcome. You're currently not signed in. Let's fix that. If this is your " \
                      "first time, please register(r). If you've previously registered, please " \
                      "connect(c). Thanks!"
                action = raw_input()
                if action == "r":
                    print "Enter a username"
                    username = raw_input()
                    print "Enter a password"
                    password = raw_input()
                    print "Enter a device alias"
                    alias = raw_input()

                    zeroZeroOne = ZeroZeroOne(username,password,"testhost",alias)
                    zeroZeroOneBuffer = version+"001"+zeroZeroOne.u +"||"+ zeroZeroOne.p +"||"+ zeroZeroOne.h +"||"+ \
                             zeroZeroOne.c +"||"+ "\\\\"
                    s.send(zeroZeroOneBuffer)
                    zeroZeroOneRecieve = s.recv(1024).decode()
                    command = zeroZeroOneRecieve[3:6]
                    body = zeroZeroOneRecieve[6:-2]
                    chunks = body.split("||")

                    if command == "501":
                        print chunks[1]
                        currentState = 2
                        currentUser = username
                        currentAlias = alias
                        currentPassword = password
                    elif command == "902":
                        print chunks[2]
                    else:
                        print chunks[0]

                elif action == "c":
                    print "Enter your username:"
                    username = raw_input()
                    print "Enter your password:"
                    password = raw_input()
                    print "Enter which device you're on:"
                    alias = raw_input()

                    zeroZeroThree = ZeroZeroThree(username,password,alias)
                    zeroZeroThreeBuffer = version+"003"+zeroZeroThree.u+"||"+zeroZeroThree.p+"||"+zeroZeroThree.c+"||"+"\\\\"
                    s.send(zeroZeroThreeBuffer)
                    zeroZeroThreeRecieve = s.recv(1024).decode()
                    command = zeroZeroThreeRecieve[3:6]
                    body = zeroZeroThreeRecieve[6:-2]
                    chunks = body.split("||")
                    if command == "503":
                        print chunks[1]
                        print chunks[2]
                        currentState = 2
                        currentUser = username
                        currentAlias = alias
                        currentPassword = password
                    elif command == "902":
                        print chunks[2]
                    else:
                        print chunks[0]
                else:
                    print "Invalid option!!!"

            elif currentState == 2:
                receive()

                print "Choose option: send(s) a message, close(x) connection or update(u) registration info."
                action = raw_input_with_timeout()

                if action == "s":
                    print "Who would you like to send this message to?"
                    recipient = raw_input()
                    print "What would you like to send?"
                    message = raw_input()
                    zeroZeroFour = ZeroZeroFour(currentUser,recipient,message)
                    zeroZeroFourBuffer = version+"004"+zeroZeroFour.s+"||"+zeroZeroFour.r+"||"+zeroZeroFour.t+"||"+ "\\\\"
                    s.send(zeroZeroFourBuffer)
                    zeroZeroFourReceive = s.recv(1024).decode()
                    command = zeroZeroFourReceive[3:6]
                    body = zeroZeroFourReceive[6:-2]
                    chunks = body.split("||")

                    if command == "504":
                        print chunks[1]
                    elif command == "902":
                        print chunks[2]
                    else:
                        print chunks[0]

                elif action == "x":
                    zeroZeroFive = ZeroZeroFive(currentUser,currentAlias)
                    zeroZeroFiveBuffer = version+"005"+zeroZeroFive.u+"||"+zeroZeroFive.c+"||"+ "\\\\"
                    s.send(zeroZeroFiveBuffer)
                    currentState = 1
                    print "Goodbye"
                    break
                elif action == "u":
                    print "What would like to update: username(u), password(p) or update alias(a)?"
                    updateAction = raw_input()

                    if updateAction == "u":
                        print "Enter a new username"
                        updateString = raw_input()
                    elif updateAction == "p":
                        print "Enter a new password"
                        updateString = raw_input()
                    elif updateAction == "a":
                        print "Enter a new alias"
                        updateString = raw_input()
                    else:
                        print "Invalid option!!!"

                    zeroZeroTwo = ZeroZeroTwo(currentUser,currentPassword,currentAlias,updateAction.upper(),updateString)
                    zeroZeroTwoBuffer = version+"002"+zeroZeroTwo.u+"||"+zeroZeroTwo.p+"||"+zeroZeroTwo.c+"||"+zeroZeroTwo.f+"||"+zeroZeroTwo.t+"||"+"\\\\"
                    s.send(zeroZeroTwoBuffer)
                    zeroZeroTwoReceive = s.recv(1024).decode()
                    command = zeroZeroTwoReceive[3:6]
                    body = zeroZeroTwoReceive[6:-2]
                    chunks = body.split("||")

                    if command == "501":
                        print chunks[1]
                        currentState = 2
                    elif command == "902":
                        print chunks[2]
                    else:
                        print chunks[0]
                elif action == "g":
                    received = s.recv(1024).decode()
                    if received != "":
                        # command = received[3:6]
                        body = received[6:-2]
                        chunks = body.split("||")
                        sender = chunks[0]
                        # recipient = chunks[1]
                        chat = chunks[2]
                        print sender + " sent you a message: " + chat

                elif action == "a":
                    continue
                else:
                    print "Invalid option!!!"
            else:
                print "Client connection suspended"
                currentState = 1

        except socket.timeout:
            currentState = 3

# main. The client state starts a 0. A new socket connection is opened to the server. If successful, the run function
# is called above.

currentState = 0
currentUser = ""
currentAlias = ""
currentPassword = ""
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get local machine name
host = socket.gethostname()
# Reserve a port for your service.
port = 9227
s.connect((host, port))
s.settimeout(1)
r = s.recv(1024).decode()

connAttempt = r
if connAttempt != "":
    currentState = 1
    print connAttempt
    run(keepOpen)
else:
    print "Connection attempt failed, please try again later."

s.close()
