#!/usr/bin/python           # This is server.py file

# https://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import json
import io
from threading import *
#from client import clientObj

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

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
        self.sock.send(b'Thank you for connecting,')
        while 1:
            received = self.sock.recv(1024).decode()
            command = received[3:6]
            body = received[6:-2]

            print command
            print body

            if command == "001":
                chunks = body.split("|")
                self.username = chunks[0]
                self.password = chunks[1]
                self.hostname = chunks[2]
                self.alias = chunks[3]

                # save registration info in db (text file for purposes of this implementation)
                data = {}
                data['username'] = self.username
                data['password'] = self.password
                data['hostname'] = self.hostname
                data['alias'] = self.alias
                with io.open('data.txt', 'w', encoding='utf-8') as datafile:
                    datafile.write(json.dumps(data,ensure_ascii=False))
                #json_data = json.dump(data)


                self.sock.send("you're registered!")



                print received

            elif command == "002":
                self.sock.send("registration updated")
                print received

            elif command == "004":
                chunks = body.split("|")
                recipient = chunks[1]
                chat = chunks[2]

                for c in connections:
                    if c.username == recipient:
                        c.sock.send(chat)


                self.sock.send("chat ack from: " + self.username)



                print connections

            elif command == "005":
                c.close()
                s.close()
            #print('Client sent:', self.sock.recv(1024).decode())
            #self.sock.send(b'Thank you for connectingggggg,')

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



