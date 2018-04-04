# vim: set ts=4 sw=4 sts=4 list nu:

import string
import queue
import time
import threading
from system import Payload
from importlib import reload, import_module

class ThreadManager:
    """ This object manages our threads. The system works by holding a local
        dictionary called self.threads. When we want to create a new thread, we
        start by finding the module containing the thread data. Once we find it
        we load the module into the dictionary (not the global module list)
        under 'module' and then instantiate the threads object and place it in
        'thread'. This gives us an easy path back to the module at any time.
    """

    def __init__(self, queues):
        """ During initilisation we import our queues, connections, conditions.
            locks, and semaphors. This is so we can pass them into our threads.
            We also create a threads queue to handle communication with the
            outside world and our dictionary to hold the modules and threads.
        """
        self.name = 'system.threadmanager'
        self.__threads = {}
        self.__queues = queues
        self.__queues.create('system.threadmanager')

    def parse_queue(self, block=False, timeout=1):
        """ We run parse_queue in a loop to check if we have any commands to
            execute within this object. When we have a command within the queue
            we remove it from the queue and then pass it into getattr. This
            then executes it localy within our object. We also place the attrs
            in the getattr function by using variadic function initiators by
            placing the '**' before the option list.
        """
        try:
            action = self.__queues.get('system.threadmanager', timeout=0.1)
            function = 'on' + action['action'].lower().capitalize()
            getattr(self, function)(**action)
        except queue.Empty:
            return
        except (KeyError, AttributeError):
            payload = Payload(self.name, action['action'], 1, 'Unknown action')
            self.__queues.put('system.interface', action['action'], payload)

    def onList(self, **kwargs):
        results = list(self.list())
        payload = Payload(self.name, 'list', 0, results)
        self.__queues.put('system.interface', 'list', payload)

    def onRead(self, **kwargs):
        for name, value in kwargs.items():
            print( '{0} = {1}'.format(name, value))

    # Fetch a list of all our threads
    def list(self):
        return self.__threads.keys()

    def create(self, module='system.interface'):
        """ due to the nature of our file system layout, we need to be able to
            specify the location that the threads module is located. to do this
            we pass in the module layout relative to the root directory of the
            neuron.py script. When we find the module, we import it into our
            local threads dictionary under the name of the thread, so an example
            for the console would be, self.threads['console']['module']. We then
            initialise and start our thread under self.dict['console']['thread']
        """
        try:
            # check if the module is in a package
            # if it is, generate the fromlist for the package and set the name to the module
            # if it isnt, copy the module name and leave the fromlist empty
            package_name, module_name = module.rsplit(".", 1)
            object_name = module_name.capitalize()
            self.__threads[module] = {}
            self.__threads[module]['module'] = import_module(module)

            # Create the thread and start it
            self.__threads[module]['thread'] = getattr(self.__threads[module]['module'], object_name) (self.__queues)
            self.__threads[module]['thread'].start()
        except KeyError:
            print('KeyError {0}: {1}'.format(id, id))

    def read(self, id=None):
        """ When we reload a thread, we need to first retrieve the module
            location from the already loaded module. We cant just reuse the
            current module because then any changes we have made wont be copied
            into the new instantiation of the thread. Once we have the name and
            location of the module, we stop the current running thread, then
            reload the module, then start the new instantiation.
        """
        if id:
            print(self.__threads[id])
        else:
            for t in threading.enumerate():
                print(t.name)

    def update(self, id):
        """ When we reload a thread, we need to first retrieve the module
            location from the already loaded module. We cant just reuse the
            current module because then any changes we have made wont be copied
            into the new instantiation of the thread. Once we have the name and
            location of the module, we stop the current running thread, then
            reload the module, then start the new instantiation.
        """
        try:
            reload(self.__threads[id]['module'])
        except Exception as error:
            print('Error reloading: {0}'.format(error))

    def delete(self, id):
        """ When we remove a thread, we first tell the thread to close itself,
            then we wait for a while and remove the reference in the threads
            dictionary. Once we are sure its gone, we remove the module also.
        """
        self.__queues.put(id,'delete',{})
        try:
             while self.__threads[id]['thread'].isAlive():
                time.sleep(0.1)
        except:
            pass

        if id in self.__threads:
            del self.__threads[id]
