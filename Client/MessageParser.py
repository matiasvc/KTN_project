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
        #print(payload)
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ValueError('Response not valid')

    def parse_error(self, payload):
        return "[Error] " + payload['content']
    
    def parse_info(self, payload):
        if payload['content'] == 'Logout successful':
            self.client.disconnect(self.client)
        return "[Info] " + payload['content']

    def parse_message(self, payload):
        return payload['sender'] + ": " + payload['content']

    def parse_history(self, payload):
        #for message in payload['content']:
            #print("hist_message: ", message)
            #self.parse(message)
        #return "History" #payload['content']
        pass
    
    # Include more methods for handling the different responses... 
