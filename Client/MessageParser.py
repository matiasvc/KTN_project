import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_msg
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        # Decode the JSON object
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            pass

    def parse_error(self, payload):
        pass
    
    def parse_info(self, payload):
        return payload["content"]

    def parse_msg(self, payload):
        pass
    
    # Include more methods for handling the different responses... 
