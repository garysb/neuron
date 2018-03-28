#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 list nu:

# Main includes
import sys
import time
import queue
import threading
from system import Queues
from system import Threader

print('Neuron: version {0} (Python {1}.{2})'.format('2.0', sys.version_info[0], sys.version_info[1]))

main = threading.current_thread()
main.name = "main"

# define our global variables
queues = Queues()
queues.create('server')
threads = Threader(queues)
threads.create('system.interface')

# Close all threads and exit
def onQuit():
    # Close all our threads
    for i in threads.threads:
        queues.put(i,'close',{})

    raise SystemExit

while True:
    try:
        # threads.threads['system.interface']['thread'].parse_queue()
        action = queues.get('server', timeout=3)
        function = 'on' + action['action'].lower().capitalize()
        globals()[function]()
    except queue.Empty:
        print('Server queue empty')
    except KeyError:
        print('Unknown action')
