#!/usr/bin/python

# server.py
# Created 05/19/2018 at 2:46PM by rossms
# This is the server implementation
# client server shell for python was ported from:
# https://www.tutorialspoint.com/python/python_networking.htm

import socket
import json
import io
import os.path
from threading import *
from messages.clientMessages import *


# global variables

version = "1.0"

# functions

# A unique clientObj is created for each connection that the server receives. You can see here that as soon as a
# client is connected, the state is changed from 0 to 1.
class clientObj(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.username = ""
        self.password = ""
        self.hostname = ""
        self.alias = ""
        self.state = 1
        self.start()

    def run(self):
        print self.addr
        print 'Got connection from', self.addr
        self.sock.send(b'Thank you for connecting.')
        while 1:
            received = self.sock.recv(1024).decode()
            command = received[3:6]
            body = received[6:-2]

            if command == "001":
                chunks = body.split("||")
                self.username = chunks[0]
                self.password = chunks[1]
                self.hostname = self.addr
                self.alias = chunks[3]

                # save registration info in db (text file for purposes of this implementation)
                data = {}
                data['username'] = self.username
                data['password'] = self.password
                data['hostname'] = self.hostname
                data['alias'] = self.alias

                try:
                    with io.open("./data/"+self.username+".txt", "w", encoding="utf-8") as datafile:
                        datafile.write(json.dumps(data, ensure_ascii=False))
                    fiveZeroOne = FiveZeroOne("R", "Registration Successful")
                    fiveZeroOneBuffer = version+"501"+fiveZeroOne.s+"||"+fiveZeroOne.t+"||"+"\\\\"
                    self.state = 2
                    self.sock.send(fiveZeroOneBuffer)
                except IOError:
                    nineZeroTwo = NineZeroTwo("User registration", "Unable to register user")
                    nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                    self.sock.send(nineZeroTwoBuffer)
                except:
                    nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                    nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                    self.sock.send(nineZeroOneBuffer)

            elif command == "002":
                if self.state == 2:
                    # find saved registration info and update it
                    chunks = body.split("||")
                    flag = chunks[3]

                    if flag == "U":
                        self.username = chunks[4]
                    else:
                        self.username = chunks[0]

                    if flag == "P":
                        self.password = chunks[4]
                    else:
                        self.password = chunks[1]

                    if flag == "A":
                        self.alias = chunks[4]
                    else:
                        self.alias = chunks[2]

                    self.hostname = self.addr
                    # save registration info in db (text file for purposes of this implementation)
                    data = {}
                    data['username'] = self.username
                    data['password'] = self.password
                    data['hostname'] = self.hostname
                    data['alias'] = self.alias

                    try:
                        if os.path.exists("./data/"+self.username+".txt"):
                            with io.open("./data/"+self.username+".txt", "w", encoding="utf-8") as datafile:
                                datafile.write(json.dumps(data,ensure_ascii=False))
                            fiveZeroOne = FiveZeroOne("R", "Registration Updated")
                            fiveZeroOneBuffer = version+"501"+fiveZeroOne.s+"||"+fiveZeroOne.t+"||"+"\\\\"
                            self.sock.send(fiveZeroOneBuffer)
                        else:
                            nineZeroTwo = NineZeroTwo("User registration", "User not found to update")
                            nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                            self.sock.send(nineZeroTwoBuffer)
                    except OSError:
                        nineZeroTwo = NineZeroTwo("User registration", "User not found to update")
                        nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                        self.sock.send(nineZeroTwoBuffer)
                    except IOError:
                        nineZeroTwo = NineZeroTwo("User registration", "Unable to register user")
                        nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                        self.sock.send(nineZeroTwoBuffer)
                    except:
                        nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                        nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                        self.sock.send(nineZeroOneBuffer)
                else:
                    nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                    nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                    self.sock.send(nineZeroOneBuffer)

            elif command == "003":
                # verify user is registered
                chunks = body.split("||")
                self.username = chunks[0]
                self.password = chunks[1]
                self.hostname = self.addr
                self.alias = chunks[3]

                try:
                    if os.path.exists("./data/"+self.username+".txt"):
                        with open("./data/"+self.username+".txt", "r") as f:
                            dataIn = json.load(f)
                            try:
                                message = dataIn["message"]
                                fiveZeroThree = FiveZeroThree("C", "Connection successful", message)
                                fiveZeroThreeBuffer = version+"503"+fiveZeroThree.s+"||"+fiveZeroThree.t+"||"+fiveZeroThree.m+"||"+"\\\\"
                                self.state = 2
                                self.sock.send(fiveZeroThreeBuffer)
                            except:
                                fiveZeroThree = FiveZeroThree("C", "Connection successful", "")
                                fiveZeroThreeBuffer = version+"503"+fiveZeroThree.s+"||"+fiveZeroThree.t+"||"+fiveZeroThree.m+"||"+"\\\\"
                                self.state = 2
                                self.sock.send(fiveZeroThreeBuffer)
                    else:
                        fiveZeroThree = FiveZeroThree("U", "Check username or register", "")
                        fiveZeroThreeBuffer = version+"503"+fiveZeroThree.s+"||"+fiveZeroThree.t+"||"+"\\\\"
                        self.sock.send(fiveZeroThreeBuffer)
                except OSError:
                    nineZeroTwo = NineZeroTwo("User registration", "User not found to update")
                    nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                    self.sock.send(nineZeroTwoBuffer)
                except IOError:
                    nineZeroTwo = NineZeroTwo("User registration", "Unable to register user")
                    nineZeroTwoBuffer = version+"902"+nineZeroTwo.a+"||"+nineZeroTwo.t+"||"+"\\\\"
                    self.sock.send(nineZeroTwoBuffer)
                except:
                    nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                    nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                    self.sock.send(nineZeroOneBuffer)

            elif command == "004":
                if self.state == 2:
                    chunks = body.split("||")
                    sender = chunks[0]
                    recipient = chunks[1]
                    chat = chunks[2]

                    try:
                        if os.path.exists("./data/"+recipient+".txt"):
                            for connection in connections:
                                if connection.username == recipient:
                                    connection.sock.send(received)
                                    break
                            else:
                                with open("./data/"+recipient+".txt", "r") as f:
                                    dataIn = json.load(f)
                                    recipientUsername = dataIn["username"]
                                    recipientPassword = dataIn["password"]
                                    recipientHostname = dataIn["hostname"]
                                    recipientAlias = dataIn["alias"]

                                    dataOut = {}
                                    dataOut['username'] = recipientUsername
                                    dataOut['password'] = recipientPassword
                                    dataOut['hostname'] = recipientHostname
                                    dataOut['alias'] = recipientAlias
                                    dataOut['message'] = "message from " + sender + ": " + chat
                                    with io.open("./data/"+recipient+".txt", "w", encoding="utf-8") as datafile:
                                        datafile.write(json.dumps(dataOut, ensure_ascii=False))

                            fiveZeroFour = FiveZeroFour("A","Message Received")
                            fiveZeroFourBuffer = version+"504"+fiveZeroFour.s+"||"+fiveZeroFour.t+"||"+"\\\\"
                            self.sock.send(fiveZeroFourBuffer)

                        else:
                            fiveZeroFour = FiveZeroFour("R","Check username")
                            fiveZeroFourBuffer = version+"504"+fiveZeroFour.s+"||"+fiveZeroFour.t+"||"+"\\\\"
                            self.sock.send(fiveZeroFourBuffer)

                    except:
                        nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                        nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                        self.sock.send(nineZeroOneBuffer)
                else:
                    nineZeroOne = NineZeroOne("Unknown error has occurred. Please try again later")
                    nineZeroOneBuffer = version+"901"+nineZeroOne.t+"||"+"\\\\"
                    self.sock.send(nineZeroOneBuffer)

            elif command == "005":
                self.state = 1
                connections.remove(self)
                self.sock.close()
                break

# main
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get local machine name
host = socket.gethostname()
# Reserve a port for your service.
port = 9227
# Bind to the port
s.bind((host, port))
# Now wait for client connection.
s.listen(5)

# empty array. As the server gets client connections, it stores them in this variable.
connections = []

# multithreading. Allows multiple client connections.
while True:
    clientsocket, address = s.accept()
    c = clientObj(clientsocket, address)
    connections.append(c)
