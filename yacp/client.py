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
        global currentState
        global currentUser
        global currentAlias

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

                t = ZeroZeroOne(username,password,"testhost",alias)
                buffer = version+"001"+t.u +"||"+ t.p +"||"+ t.h +"||"+ t.c +"||"+ "\\\\"
                s.send(buffer)
                r = s.recv(1024).decode()
                command = r[3:6]
                body = r[6:-2]
                chunks = body.split("||")

                if command == "501":
                    print chunks[1]
                    currentState = 2
                    currentUser = username
                    currentAlias = alias
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

                t = ZeroZeroThree(username,password,alias)
                buffer = version+"003"+t.u+"||"++t.p+"||"++t.a+"||"+"\\\\"
                s.send(buffer)
                r = s.recv(1024).decode()
                command = r[3:6]
                body = r[6:-2]
                chunks = body.split("||")

                if command == "503":
                    print chunks[1]
                    currentState = 2
                    currentUser = username
                    currentAlias = alias
                elif command == "902":
                    print chunks[2]
                else:
                    print chunks[0]
            else:
                print "Invalid option!!!"

        elif currentState == 2:
            print "Choose option: send(s) a message, close(x) connection or update(u) registration info."
            action = raw_input()

            if action == "s":
                print "Who would you like to send this message to?"
                recipient = raw_input()
                print "What would you like to send?"
                message = raw_input()
                t = ZeroZeroFour(currentUser,recipient,message)
                buffer = version+"004"+t.s+"||"+t.r+"||"+t.t+"||"+ "\\\\"
                s.send(buffer)
                r = s.recv(1024).decode()
                command = r[3:6]
                body = r[6:-2]
                chunks = body.split("||")

                if command == "504":
                    print chunks[1]
                elif command == "902":
                    print chunks[2]
                else:
                    print chunks[0]

            elif action == "x":
                t = ZeroZeroFive(currentUser,currentAlias)
                buffer = version+"005"+t.u+"||"+t.c+"||"+ "\\\\"
                s.send(buffer)
                currentState = 1
                break
            elif action == "u":
                print "u"
            else:
                print "Invalid option!!!"
        else:
            print "suspended"


        # print "Choose option: Register(r), update(u), send(s), close(x), get(g)"
        # action = raw_input()
        #
        #
        #
        # if action == "u":
        #     t = ZeroZeroOne("testuser","testpass","testhost","testalias")
        #     buffer = "1.0"+"002"+t.u +"|"+ t.p +"|"+ t.h +"|"+ t.c +"|"+ "\\\\"
        #     s.send(buffer)
        #     r = s.recv(1024).decode()
        #     print r
        #
        # if action == "s":
        #     t = ZeroZeroFour("testuser1","testuser2","hey there")
        #     buffer = "1.0"+"004"+t.s+"|"+t.r+"|"+t.t+"|"+ "\\\\"
        #     s.send(buffer)
        #     r = s.recv(1024).decode()
        #     print r
        #
        # if action == "x":
        #     t = ZeroZeroFive("testuser","testalias")
        #     buffer = "1.0"+"005"+t.u+"|"+t.c+"|"+ "\\\\"
        #     s.send(buffer)
        #     break
        #
        # if action =="g":
        #     r = s.recv(1024).decode()
        #     print r

# main
currentState = 0
currentUser = ""
currentAlias = ""

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
r = s.recv(1024).decode()

connAttempt = r
if connAttempt != "":
    currentState = 1
    print connAttempt
    run(keepOpen)
else:
    print "Connection attempt failed, please try again later."


#print action

#print(r[:1])


#s.close                     # Close the socket when done





# TODO: All client to server messages

# TODO : keep client connection open

# TODO : how to handle user actions through CL?

# TODO: : DFA

