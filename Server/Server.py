# -*- coding: utf-8 -*-

import socketserver
import json
from time import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clients = {}
messageHistory = []


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
        self.username = None

        self.handlers = {
            'login': self.handle_login,
            'msg': self.handle_message
        }

        # Loop that listens for messages from the client
        while True:
            data = self.connection.recv(4096)
            if data:
                received_dict = json.loads(data.decode('utf-8'))
                messageType = received_dict['request']
                print("Server received: " + str(received_dict))

                self.handlers[messageType](received_dict)

    def handle_login(self, received_dict):
        username = received_dict["content"]
        if username in clients.keys():
            response_dict = {"timestamp": time(), "sender": "Server", "response": "error", "content": "Username taken"}
        else:
            response_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "Login successful!"}
            self.username = username
            self.send_to_client(response_dict)

            # Return history to client
            for history_message_dict in messageHistory:
                self.send_to_client(history_message_dict)

            info_message_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "User joined: " + username}
            self.broadcast(info_message_dict)
            clients[username] = self

    def handle_message(self, received_dict):
        for client in clients.values():
            client.receive_message(self.username, received_dict["content"])

    def send_to_client(self, content_dict):
        content_string = json.dumps(content_dict)
        print("Server sent: " + content_string)
        self.connection.sendall(bytes(content_string, 'utf-8'))

    def broadcast(self, content_dict):
        messageHistory.append(content_dict)
        for client in clients.values():
            client.send_to_client(content_dict)

    def receive_message(self, sender, message):
        content = {"timestamp": time(), "sender": sender, "response": "message", "content": message}
        self.send_to_client(content)


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
