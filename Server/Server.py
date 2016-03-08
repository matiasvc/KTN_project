# -*- coding: utf-8 -*-

import socketserver
import json, re
from time import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

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
        self.user = None
        server.clients.append(self)

        self.handlers = {
            'login' : self.login,
            'logout' : self.logout,
            'msg' : self.message,
            'names' : self.names,
            'help' : self.help
        }

        # Loop that listens for messages from the client
        while True:
            try:
                data = self.connection.recv(4096)
            except Exception as e:
                #self.logout()
                break

            if data:
                recivedDict = json.loads(data.decode('utf-8'))
                messageType = recivedDict['request']
                if 'content' in recivedDict:
                    content = recivedDict['content']

                    print("Server received: " + str(recivedDict))

                    response = self.handlers[messageType](content)
                else:
                    print("Server received: " + str(recivedDict))

                    response = self.handlers[messageType]()

                if response:
                    self.send(response)

    def history(self):
        msg = {"timestamp":time(), "sender":"[Server]", "response":"history", "content":[]}
        for message in server.messages:
            msg['content'].append(message)
        print("History: ", msg)
        self.send(msg)

    def login(self, content):
        if re.match("[A-Za-z0-9_-]+$", content):
            self.user = content

            #self.history()

            if self.user in server.clients:
                response = {"timestamp":time(), "sender": "[Server]", "response": "error", "content": "Username taken"}
            else:
                response = {"timestamp":time(), "sender": "[Server]", "response": "info", "content": "Login successfull!"}
                for client in server.clients:
                    infoMessage = {"timestamp":time(), "sender": "[Server]", "response": "info", "content": "User joined: " + self.user}
                    client.send(infoMessage)
            server.messages.append(infoMessage)
        else:
            response = {"timestamp":time(), "sender": "[Server]", "response": "info", "content": "Invalid username"}
        return response

    def logout(self):
        #print("Clients: ", server.clients)
        #print("Self: ", self)
        server.clients.remove(self)
        self.connection.close()
        if (self.user != None):
            print(self.user, 'logged out')
            msg = {'timestamp':time(), 'sender':'[Server]', 'response':'info', 'content':self.user+' disconnected'}
            for client in server.clients:
                if (client.user != None):
                    client.send(msg)
            server.messages.append(msg)

    def message(self, content):
        for client in server.clients:
            client.receiveMessage(client.user, content)

    def names(self):
        names = ""
        for username in server.clients:
            names += username.user+', '
        content = {'timestamp':time(), 'sender':'[Server]', 'response':'info', 'content':'Connected users: '+names}
        self.send(content)

    def help(self):
        msg = {'timestamp':time(), 'sender':'[Help]', 'response':'info', 'content':'Available commands: login <username>, logout, msg <message>, names, help'}
        self.send(msg)

    def send(self, content):
        contentString = json.dumps(content)
        print("Server sent: " + contentString)
        self.connection.send(bytes(contentString, 'utf-8'))

    def receiveMessage(self, user, message):
        content = {"timestamp":time(), "sender": user, "response": "message", "content": message}
        self.send(content)
        server.messages.append(content)

    def error(self, content):
        msg_holder = {'timestamp':time(), 'sender':'[Error]', 'response':'error', 'content':content}
        self.send(msg_holder)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True
    clients = []
    messages = []

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
