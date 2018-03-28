# vim: set ts=4 sw=4 sts=4 list nu:

import queue
import bisect
import json

# Extend PriorityQueue to let us run multiple queues at once
class Queues:
    def __init__(self):
        # Create a blank dictionary
        self.queues = {}

    # Fetch a list of all our queues
    def list(self):
        return self.queues.keys()

    # Add a queue to the list
    def create(self, thread):
        self.queues[thread] = queue.PriorityQueue(0)

    # Remove a queue from the list
    def remove(self, thread):
        del self.queues[thread]

    # Put an item in a queue
    def put(self, thread, action, args='', priority=0, block=True, timeout=None):
        try:
            self.queues[thread].put({'priority': priority, 'action': action, 'arguments': args}, block, timeout)
        except:
            pass

    # Get a value from the queue
    def get(self, thread, block=True, timeout=None):
        return self.queues[thread].get(block, timeout)

    # Get the size of a queue
    def size(self, thread):
        return self.queues[thread].qsize()

    # return true if queue is empty
    def empty(self, thread):
        return self.queues[thread].empty()

    # Flush data in a queue
    def flush(self,thread):
        return

    # Return true if queue is full
    def full(self, thread):
        return self.queues[thread].full()

    # Fetch item from a queue without waiting
    def get_nowait(self, thread):
        return self.queues[thread].get_nowait()

    # Put item on queue without waiting
    def put_nowait(self, thread, function, args='', priority=0):
        return self.queues[thread].put_nowait((priority, function, args))
