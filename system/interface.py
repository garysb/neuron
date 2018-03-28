# vim: set ts=4 sw=4 sts=4 list nu:
# import sys
# import time
import asyncio
import queue
# import datetime
import websockets
from system import Payload
from system import Thread

class Interface(Thread):
    def __init__(self, queues):
        Thread.__init__(self, queues)
        print('Websocket version: ', websockets.version.version)

    # Default instant
    def run (self):
        self.setName('system.interface')
        self.queues.create(self.getName())

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        start_server = websockets.serve(self.handler, '127.0.0.1', 1234)
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    async def consumer(self, message):
        payload = Payload()
        payload.load(message)
        print('Neuron: consumer - {0}'.format(payload.generate()))

        # add the payload to the queue stack
        self.queues.put(payload.thread, payload.action, payload, payload.priority)
        return

    async def producer(self):
        payload = Payload()
        payload.thread = 'system.interface'
        payload.action = 'reset'
        payload.status = '0'
        payload.data = 'Successfully Reset'

        print('Neuron: producer - {0}'.format(payload.generate()))
        return payload.generate()

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consumer(message)

    async def producer_handler(self, websocket, path):
        while True:
            try:
                action = self.queues.get(self.getName(), True, timeout=0.25)
                print('Action: {0}'.format(action))
                message = await self.producer()
                await websocket.send(message)
            except queue.Empty:
                print('system.interface queue empty')
                pass

    async def handler(self, websocket, path):
        print('Neuron: handler')
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket, path))
        producer_task = asyncio.ensure_future(self.producer_handler(websocket, path))
        done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,)

        for task in pending:
            task.cancel()
