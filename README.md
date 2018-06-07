# YACP - Yet Another Chat Protocol


## Requirements and Prerequisites
1. YACP is implemented in Python. Specifically, python v2.7. It needs python installed, and has been tested on linux with bash and zsh.


## Execution:
1. In one terminal window, cd into the yacp folder.
2. Start the server: `python server.py`
3. In a separate terminal window, start a client `python client.py`
4. In a third terminal, start an additional instance of the client `python client.py`

I did not implement the extra credit.

[![demo run](http://img.youtube.com/vi/VqUbPONZT-c/0.jpg)](https://www.youtube.com/watch?v=VqUbPONZT-c "demo run")

## About YACP:

### Structure
Client.py is the client implementation, server.py is the server implementation, and
messages/clientMessages.py are the messages. Data is stored in /data/[username].txt in json format.

### DFA
Both the client and the server check for the current state of the client instance when making calls the server.

The DFA states can be seen below.

    currentState = 0 : Disconnected
    currentState = 1 : Connected, but not signed in
    currentState = 2 : Connected, signed in
    currentState = 3 : Signed in, suspended

This state checking can be seen in both client.py, and server.py. When the client first connects, it is set with currentState =0. Once connected to the server, the currentState is set to 1. Once ‘signing in’ which means user is registered currentState = 2. Both the server and client check state to ensure that commands are only reachable if the currentState meets the requirements for those actions.

### Concurrent
YACP handles multiple clients with a threading model. Each new client is handled with a new instance of the ClientObj by the server (server.py). The server keeps track of all the current client connections, which is how it knows if it should send messages directly to recipients, or should store them for the next time the intended receiver connects. I have not stress tested this, but works well with 2-4 connections during local testing.

### Service
YACP binds to port number 9227 (Y-A-C-P). This can be seen in both client.py and server.py. For the purposes of this implementation, it is running on localhost. When a new client connects to the server, the running server task prints out the connection details from the client. This is the only output from server.py.

### Client
By default the client gets the hostname of the local machine, and then connects to the port number where the server is listening on (client.py). Future implementations would use the IP address provided for the server machine. When a client connects to the server, its socket address is saved in the server connections, which is how the server knows who is on the end of each connection. This is how the server knows which client to send chat messages to.

### UI
For this implementation, all user interaction is handled through a CLI (client.py). The details of the messages are encapsulated in the client implementation, and prompts the user for information required to build those message details. The only “gotcha” here is that once connected, The client will print the default list of actions repeatedly. This is due to the polling functionality where the client checks to see if the server has sent any messages. Future implementations of a more graphical UI would encapsulate this polling and hide it from the user.

### Robust
This implementation checks to ensure that the message code is recognized, and then sends / receives messages based on that value. However, because the information is not encrypted (for this implementation, although it would be in the future) packet sniffing might reveal its contents. All OS and IO operations are wrapped in a try block, and depending on the exception throw, either a 901 or a 902 error message is returned to the user.
