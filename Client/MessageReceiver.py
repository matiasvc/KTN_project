# -*- coding: utf-8 -*-
from threading import Thread
from socket import *
import json


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True

        self.client = client
        self.connection = connection

        self.run()

    def run(self):
        json_response = self.connection.recv(1024)
        self.client.receive_message(json_response)
