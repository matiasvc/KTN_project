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

        self.message_reciever = MessageReceiver(self, self.connection)
        self.message_parser = MessageParser()

        self.received_answer = True

        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.message_reciever.start()
        while True:
            self.get_input()


    def get_input(self):
        if self.received_answer:
            inputString = input(">>")
            parts = inputString.split(" ", 1)
            request = None
            content = None
            if len(parts) == 2:
                command = parts[0]
                argument = parts[1]
                if command == "login":
                    request = "login"
                    content = argument
                elif command == "msg":
                    request = "msg"
                    content = argument
            else:
                command = inputString
                if command == "logout":
                    request = "logout"
                elif command == "names":
                    request = "names"
                elif command == "help":
                    request = "help"

            if not request:
                print("Invalid input")
            else:
                requestDict = {'request': request, 'content': content}
                jsonData = json.dumps(requestDict)
                self.send_payload(jsonData)


    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print(self.message_parser.parse(message))
        self.received_answer = True

    def send_payload(self, data):
        self.received_answer = False
        self.connection.sendall(bytes(data, 'utf-8'))


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    print('Type "login <username>" to log in ')
    client = Client('localhost', 9998)

