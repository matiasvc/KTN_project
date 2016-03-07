import json

class MessageParser():
    def __init__(self, client):


        self.client = client

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history

        }

    def parse(self, payload):
        # Decode the JSON object
        payload = json.loads(payload.decode('utf-8'))

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ValueError('Response not valid')

    def parse_error(self, payload):
        return payload['content']
    
    def parse_info(self, payload):
        if payload['content'] == 'Logout succesful':
            self.client.disconnect(self.client)
         return payload['content']

    def parse_message(self, payload):
        return payload['message']

    def parse_history(self, payload):
        return json.loads(payload['content'].decode('utf-8'))
    
    # Include more methods for handling the different responses... 
