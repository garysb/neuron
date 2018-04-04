#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 list nu:

# main includes
import sys
import queue
import threading
from system import QueueManager
from system import ThreadManager
from system import Payload

# name our main thread, then print the version and python version
main = threading.current_thread()
main.name = "main"
print('Neuron: version {0} (Python {1}.{2})'.format(
    '2.0',
    sys.version_info[0],
    sys.version_info[1])
)

# define our global variables
qm = QueueManager()
qm.create('server')
tm = ThreadManager(qm)
tm.create('system.interface')

# close all threads and exit
def onExit():
    # loop through the threads and close them
    try:
        for i in tm.list():
            tm.delete(i)
    except:
        # there was a problem closing some threads
        raise Exception
    finally:
        # we have closed all the threads, exit the system
        raise SystemExit

while True:
    try:
        tm.parse_queue()
        action = qm.get('server', timeout=0.1)
        function = 'on' + action['action'].lower().capitalize()
        globals()[function]()
    except queue.Empty:
        pass
    except KeyError:
        payload = Payload('server', action['action'], 1, 'Unknown action')
        qm.put('system.interface', action['action'], payload)
    except KeyboardInterrupt:
        print('Shutting down server')
        onExit()
