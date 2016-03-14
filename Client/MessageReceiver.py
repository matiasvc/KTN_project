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
        self.client = client
        self.connection = connection
        super(MessageReceiver, self).__init__()
        # Flag to run thread as a deamon
        self.daemon = True
        self.should_stop = False

    def run(self):
        while True:
            json_response = self.connection.recv(1024)
            if json_response:
                self.client.receive_message(json_response)
