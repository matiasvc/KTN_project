# -*- coding: utf-8 -*-

import socketserver
import json
from time import time, sleep
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
            'msg': self.handle_message,
            'logout': self.handle_logout,
            'help' : self.handle_help,
            'history' : self.handle_history,
            'names' : self.handle_names
        }

        # Loop that listens for messages from the client
        while True:
            try:
                data = self.connection.recv(4096)
                if data:
                    received_dict = json.loads(data.decode('utf-8'))
                    messageType = received_dict['request']
                    print("Server received: " + str(received_dict))
                    try:
                        self.handlers[messageType](received_dict)
                    except KeyError:
                        self.handle_unknow_command(received_dict)
            except ConnectionResetError:
                if self.username:
                    print("Connection reset: " + self.username)
                    del clients[self.username]

    def handle_login(self, received_dict):
        username = received_dict["content"]
        if username in clients.keys():
            response_dict = {"timestamp": time(), "sender": "Server", "response": "error", "content": "Username taken"}
            self.send_to_client(response_dict)
        else:
            response_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "Login successful!"}
            self.username = username
            self.send_to_client(response_dict)

            # Return history to client
            self.send_history_to_client()

            info_message_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "User joined: " + username}
            self.broadcast(info_message_dict)
            clients[username] = self

    def handle_logout(self, received_dict):
        del clients[self.username]
        response_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "Logout successful"}
        self.send_to_client(response_dict)
        info_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": "User left: " + self.username}
        self.broadcast(info_dict)

    def handle_message(self, received_dict):
        message_dict = {"timestamp": time(), "sender": self.username, "response": "message", "content": received_dict["content"]}
        messageHistory.append(message_dict)
        for client in clients.values():
            client.send_to_client(message_dict)

    def handle_history(self, received_dict):
        self.send_history_to_client()

    def handle_help(self, received_dict):
        help_string = "Commands:\n" \
                      "login [username] - Log in to server\n" \
                      "msg [message - Send message]\n" \
                      "logout - Log out from server\n" \
                      "help - Print this page\n" \
                      "history - Print a history of all messages"
        response_dict = {"timestamp": time(), "sender": "Server", "response": "info", "content": help_string}
        self.send_to_client(response_dict)

    def handle_names(self, received_dict):
        name_list = list(clients.keys())
        response_dict = {"timestamp": time(), "sender": "Server", "response": "names", "content": name_list}
        self.send_to_client(response_dict)

    def handle_unknow_command(self, received_dict):
        response_dict = {"timestamp": time(), "sender": "Server", "response": "error", "content": "Unknown command: " + received_dict['request']}
        self.send_to_client(response_dict)

    def send_to_client(self, content_dict):
        content_string = json.dumps(content_dict)
        print("Server sent: " + content_string)
        self.connection.sendall(bytes(content_string, 'utf-8'))

    def send_history_to_client(self):
        history_string = json.dumps(messageHistory)
        history_dict = {"timestamp": time(), "sender": "Server", "response": "history", "content": history_string}
        self.send_to_client(history_dict)

    def broadcast(self, content_dict):
        for client in clients.values():
            client.send_to_client(content_dict)



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
    HOST, PORT = '0.0.0.0', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
