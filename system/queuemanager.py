# vim: set ts=4 sw=4 sts=4 list nu:

# imports
import json
import queue
import bisect
import threading
from system import Payload

# extend PriorityQueue to let us run multiple queues at once
class QueueManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Create a blank dictionary
        self.__queues = {}
        self.setName('system.queuemanager')
        self.create(self.getName())

    def run(self):
        while True:
            self.parse_queue()

    def parse_queue(self, block=True, timeout=0.25):
        """ We "pop" an item off the start of the queue by calling get method.
            Once we have the item in a list, we grab the function name and
            arguments to call. The arguments are placed into the method using a
            variadic call by prepending the ** to the beginning of the argument.
        """
        try:
            action = self.get(self.getName(), timeout=0.1)
            function = 'on' + action['action'].lower().capitalize()
            getattr(self, function)(**action)
        except (KeyError, AttributeError):
            payload = Payload(self.getName(), action['action'], 1, 'Unknown action')
            self.put('system.interface', action['action'], payload)
        except queue.Empty:
            pass

    def onList(self, **kwargs):
        results = list(self.list())
        payload = Payload(self.name, 'list', 0, results)
        self.put('system.interface', 'list', payload)

    def onCreate(self, **kwargs):
        try:
            for name, value in kwargs.items():
                print( '{0} = {1}'.format(name, value))

            self.create('tester')
            payload = Payload(self.name, 'create', 0)
            self.put('system.interface', 'create', payload)
        except:
            payload = Payload(self.name, 'create', 1, 'Error creating queue')
            self.put('system.interface', 'create', payload)

    # fetch a list of all our queues
    def list(self):
        return self.__queues.keys()

    # Add a queue to the list
    def create(self, thread):
        self.__queues[thread] = queue.PriorityQueue(0)

    # Remove a queue from the list
    def remove(self, thread):
        del self.__queues[thread]

    # Put an item in a queue
    def put(self, thread, action, args='', priority=0, block=True, timeout=None):
        try:
            self.__queues[thread].put({'priority': priority, 'action': action, 'arguments': args}, block, timeout)
        except:
            pass

    # Get a value from the queue
    def get(self, thread, block=True, timeout=None):
        return self.__queues[thread].get(block, timeout)

    # Get the size of a queue
    def size(self, thread):
        return self.__queues[thread].qsize()

    # return true if queue is empty
    def empty(self, thread):
        return self.__queues[thread].empty()

    # Flush data in a queue
    def flush(self,thread):
        return

    # Return true if queue is full
    def full(self, thread):
        return self.__queues[thread].full()

    # Fetch item from a queue without waiting
    def get_nowait(self, thread):
        return self.__queues[thread].get_nowait()

    # Put item on queue without waiting
    def put_nowait(self, thread, function, args='', priority=0):
        return self.__queues[thread].put_nowait((priority, function, args))
