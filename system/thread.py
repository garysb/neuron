# vim: set ts=4 sw=4 sts=4 list nu:

import threading
import queue
from system import Payload

class Thread(threading.Thread):
    """Create our threading template. Any changes in this class are reflected
        accross all threads.
    """
    def __init__(self, queues):
        """ Initiate our object ensuring we call any init needed for the main
            threading object.
        """
        threading.Thread.__init__(self)
        self.queues = queues

    def send(self, data, priority=100, action='', status=0):
        """ Send a message to the Websocket Interface """
        # create the Payload
        payload = Payload()
        payload.thread = self.getName()
        payload.priority = 100
        payload.action = action
        payload.status = status
        payload.data = data

        self.queues.put('system.interface', 'send', payload, priority=priority, block=True, timeout=None)

    def parse_queue(self, block=True, timeout=0.25):
        """ We "pop" an item off the start of the queue by calling get method.
            Once we have the item in a list, we grab the function name and
            arguments to call. The arguments are placed into the method using a
            variadic call by prepending the ** to the beginning of the argument.
        """
        try:
            action = self.queues.get(self.getName(), block=block, timeout=timeout)
            function = 'on' + action['action'].lower().capitalize()
            getattr(self, function)(*action['action'])
        except (KeyError, AttributeError):
            print('Unknown action "{0}" in "{1}"'.format(function, self.getName()))
        except queue.Empty:
            print('No action for {0}'.format(self.getName()))
            return

    # def parse_action(self, action):
    # 	""" When we are running the system, we dont want to be stuck into using
    # 		one interface type. By executing the commands locally and returning
    # 		the result to the calling party, we can get around this. Just note
    # 		that we get the whole command here, so we need to first strip off
    # 		the 'threads' part. Also, all commands should be placed into the
    # 		queue and not run dirrectly. This is so that our prioritising works
    # 		properly.
    # 	"""
    # 	try:
    # 		if len(action) == 1:
    # 			action.append('read')

    # 		call = getattr(self, action[1], None)

    # 		if callable(call):
    # 			values = dict([v.split(':') for v in action[2:]])
    # 			self.queues.put(action[0], action[1], values)
    # 		else:
    # 			print('{0} action not found in {1}'.format(action[1], action[0]))
    # 	except:
    # 		print('error calling {0} in {1}'.format(action[0], action[1]))

    # #def send(self, thread, function, args='', priority=0, block=True, timeout=None):
    # #	""" Send a message to another thread queue
    # #	"""
    # #	self.s_queues.put(thread=thread, function=function, args=args, priority=priority, block=block, timeout=timeout)

    # def output(self, message):
    # 	""" When we are running the system, we dont want to be stuck into using
    # 		one interface type. By executing the commands locally and returning
    # 		the result to the calling party, we can get around this. Just note
    # 		that we get the whole command here, so we need to first strip off
    # 		the 'threads' part. Also, all commands should be placed into the
    # 		queue and not run dirrectly. This is so that our prioritising works
    # 		properly.
    # 	"""
    # 	self.queues.write(self.name, message)

    def onClose(self):
    	""" Close the thread
    	"""
    	# Remove our queue
    	self.queues.remove(self.getName())

    	# Cant use the exit() call as this invokes string __exit__
    	raise SystemExit
