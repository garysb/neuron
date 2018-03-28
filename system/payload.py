import json

# Payload Object
class Payload(object):

    def __init__(self, thread=None, action=None, status=None, data=None, priority=None):
        if priority is None:
            priority = 100
        self.priority = priority
        self.thread = thread
        self.action = action
        self.status = status
        self.data = data

    def load(self, data):
	    self.__dict__ = json.loads(data)


    def generate(self):
        return json.dumps(self.__dict__)
