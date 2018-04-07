# tasks to be completed

## repository
- build a pre-commit hook for coding standards [https://github.com/pre-commit/pre-commit-hooks/tree/master/pre_commit_hooks]
- build a pre-commit hook for unit testing
- define release cycle

## server
- switch to using Socket.IO, first need to find an elegant way without requiring a external server
- remake neuron-db as a thread and switch to using MongoDB as the storage engine
- figure out a proper structure for Payloads that handles arguments for object commands
- look into using RabitQM for queue management instead of our custom queue manager
- figure out the proper file structure: eg. where should IBM Q processore go?
- add connections controller back in with some example connections to devices
- create a data mining module to process Wikipedia/dictionaries/image sets to train the neural network
- add the ability to process images (Intel OpenCV or other?)

## client
- switch to using Socket.IO
- change the terminal output syntax to not show the payload directly
- create the thread manager view to show current thread list, status, memory used
- create the queue manager view to show all queues and queue sizes
- create the genetics view to show the evolution tree and current DNA
- create the memory view to show a 3D (WebGL) model of the memory and the strengths of connections between neurons
- create the geo-spacial view to show body locations and obsticles in memory
- create the bodys views to show body data
- create the server view to show server status and client connections
- add functionality to allow clients to chat with the neural network (could be through the current terminal)
