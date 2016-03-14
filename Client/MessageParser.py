import json

class MessageParser():
    def __init__(self, client):


        self.client = client

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'names': self.parse_names

        }

    def parse(self, payload):
        # Decode the JSON object
        payload = json.loads(payload.decode('utf-8'))
        print(payload)
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ValueError('Response not valid')

    def parse_error(self, payload):
        return payload['content']
    
    def parse_info(self, payload):
        return payload['content']

    def parse_message(self, payload):
        return payload['sender'] + ": " + payload['content']

    def parse_names(self, payload):
        names = payload['content']
        mess = "Users in lobby:" + "\n"
        for name in names:
            mess += name + "\n"
        return mess

    def parse_history(self, payload):
        json_list = json.loads(payload['content'])
        mess = ""
        for item in json_list:
            mess += self.parse_message(item) + "\n"
        return mess
    
    # Include more methods for handling the different responses... 
