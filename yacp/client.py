#!/usr/bin/python           # This is client.py file

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from messages.clientMessages import *
from threading import *

# global variables
version = "1.0"
keepOpen = 1

# functions
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
                received = s.recv(1024).decode()
                if received != "":
                    body = received[6:-2]
                    chunks = body.split("||")
                    sender = chunks[0]
                    chat = chunks[2]
                    print sender + " sent you a message: " + chat
                print "Choose option: send(s) a message, close(x) connection or update(u) registration info."
                action = raw_input()

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

                else:
                    print "Invalid option!!!"
            else:
                print "Client connection suspended"
                currentState = 1

        except socket.timeout:
            currentState = 3

# main
currentState = 0
currentUser = ""
currentAlias = ""
currentPassword = ""

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 9227                # Reserve a port for your service.

s.connect((host, port))
r = s.recv(1024).decode()

connAttempt = r
if connAttempt != "":
    currentState = 1
    print connAttempt
    run(keepOpen)
else:
    print "Connection attempt failed, please try again later."

s.close()

# TODO : how to handle user actions through CL?

# TODO: : DFA

