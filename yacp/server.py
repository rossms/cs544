#!/usr/bin/python           # This is server.py file

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import json
import io
import os.path
from threading import *
from messages.clientMessages import *
#from client import clientObj

# global variables

version = "1.0"

# functions

class clientObj(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.username = ""
        self.password = ""
        self.hostname = ""
        self.alias = ""
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
                print received
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

            elif command == "003":
                # verify user is registered
                self.sock.send("connected")
                print received

            elif command == "004":
                chunks = body.split("||")
                recipient = chunks[1]
                chat = chunks[2]

                fiveZeroFour = FiveZeroFour("A","Message Received")
                fiveZeroFourBuffer = version+"504"+fiveZeroFour.s+"||"+fiveZeroFour.t+"||"+"\\\\"
                self.sock.send(fiveZeroFourBuffer)
                # TODO : if user or recipient is unknown, send back an error


                for c in connections:
                    if c.username == recipient:
                        c.sock.send(chat)
                # TODO : if recipient is not in connections, store message for next connection
                #print connections

            elif command == "005":
                self.sock.close()
                s.close()
                #c.close()

                #s.close()
            #print('Client sent:', self.sock.recv(1024).decode())
            #self.sock.send(b'Thank you for connectingggggg,')

# main

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 9227                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

# TODO: multithreading
#c, addr = s.accept()     # Establish connection with client.
#print 'Got connection from', addr
#c.send('Thank you for connecting')

connections = []

while True:
    clientsocket, address = s.accept()
    c = clientObj(clientsocket, address)
    connections.append(c)


# TODO: : DFA

# TODO : User registration

# TODO : Chat



