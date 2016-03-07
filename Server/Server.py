# -*- coding: utf-8 -*-

import socketserver
import json
from time import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clients = {}


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.handlers = {
            'login' : self.handleLogin,
            'msg' : self.handleMessage
        }

        # Loop that listens for messages from the client
        while True:
            data = self.connection.recv(4096)
            if data:
                recivedDict = json.loads(data.decode('utf-8'))
                messageType = recivedDict['request']
                content = recivedDict['content']

                print("Server received: " + str(recivedDict))

                response = self.handlers[messageType](content)

                if response:
                    self.send(response)


    def handleLogin(self, content):
        # TODO: Check if username is taken
        response = {"timestamp":time(), "sender": "Server", "response": "info", "content": "Login successfull!"}
        username = content

        clients[username] = self
        return response

    def handleMessage(self, content):
        for username, client in clients.items():
            if client != self:
                client.receiveMessage(username, content)

    def send(self, content):
        contentString = json.dumps(content)
        print("Server sent: " + contentString)
        self.connection.sendall(bytes(contentString, 'utf-8'))

    def receiveMessage(self, user, message):
        content = {"timestamp":time(), "sender": user, "response": "message", "content": message}
        self.send(content)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
