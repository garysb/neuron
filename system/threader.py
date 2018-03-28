# vim: set ts=4 sw=4 sts=4 list nu:

import string
import queue
import threading
from importlib import reload, import_module

class Threader:
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
        self.name = 'system.threader'
        self.threads = {}
        self.queues = queues
        self.queues.create('system.threader')

    # Fetch a list of all our queues
    def list(self):
        return self.threads.keys()

    def parse_queue(self, block=False, timeout=1):
        """ We run parse_queue in a loop to check if we have any commands to
            execute within this object. When we have a command within the queue
            we remove it from the queue and then pass it into getattr. This
            then executes it localy within our object. We also place the attrs
            in the getattr function by using variadic function initiators by
            placing the '**' before the option list.
        """
        while True:
            try:
                runner = self.queues.get('system.threader', block=block, timeout=timeout)
                getattr(self, runner[1])(**runner[2])
            except queue.Empty:
                print('system.threader queue empty')
                return

    def parse_action(self, action):
        """ When we are running the system, we dont want to be stuck into using
            one interface type. By executing the commands locally and returning
            the result to the calling party, we can get around this. Just note
            that we get the whole command here, so we need to first strip off
            the 'threads' part. Also, all commands should be placed into the
            queue and not run dirrectly. This is so that our prioritising works
            properly.
        """
        try:
            if len(action) == 1:
                action.append('read')

            call = getattr(self, action[1], None)

            if callable(call):
                values = dict([v.split(':') for v in action[2:]])
                self.queues.put(action[0], action[1], values)
            else:
                print("%s action not found in %s" % {action[1], action[0]})
        except:
            print("error calling %s in %s" % {action[0], action[1]})

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
            self.threads[module] = {}
            self.threads[module]['module'] = import_module(module)

            # Create the thread and start it
            self.threads[module]['thread'] = getattr(self.threads[module]['module'], object_name) (self.queues)
            self.threads[module]['thread'].start()
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
            print(self.threads[id])
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
            module = self.threads[id]['module'].__name__
            reload(self.threads[id]['module'])
        except Exception as error:
            print('Error reloading: {0}'.format(error))

    def delete(self, id):
        """ When we remove a thread, we first tell the thread to close itself,
            then we wait for a while and remove the reference in the threads
            dictionary. Once we are sure its gone, we remove the module also.
        """
        self.queues.put(id,'close',{})
        try:
            while self.threads[id]['thread'].isAlive():
                time.sleep(1)
        except:
            pass
        if self.threads.has_key(id):
            del self.threads[id]
