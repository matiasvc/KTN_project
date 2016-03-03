# -*- coding: utf-8 -*-
from socket import *
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    username = ""

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        username = raw_input("Enter username: ")
        loginRequest = {'request': 'login', 'content': username}
        jsonLogin = json.dumps(loginRequest)
        self.send_payload(jsonLogin)
        
    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.sendall(data)
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
