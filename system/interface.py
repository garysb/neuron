#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 list nu:

import asyncio
import queue
import json
import websockets
from system import Payload
from system import Thread

class Interface(Thread):

    def __init__(self, queues):
        Thread.__init__(self, queues)
        print('Websocket version: ', websockets.version.version)

    def run(self):
        self.setName('system.interface')
        self.queues.create(self.getName())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.incoming = asyncio.Queue()
        self.outgoing = asyncio.Queue()

        asyncio.set_event_loop(self.loop)
        start_server = websockets.serve(self.handler, '127.0.0.1', 1234)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, websocket, path):
        self.ws = websocket

        while True:
            listener_task = asyncio.ensure_future(self.get_message())
            producer_task = asyncio.ensure_future(self.produce())
            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)

            if listener_task in done:
                await self.consume()
            else:
                listener_task.cancel()

            if producer_task in done:
                msg_to_send = producer_task.result()
                await self.send_message(msg_to_send)
            else:
                producer_task.cancel()

    async def get_message(self):
        msg_in = await self.ws.recv()
        await self.incoming.put(msg_in)
        payload = Payload()
        payload.load(msg_in)

        # add the payload to the queue stack
        self.queues.put(payload.thread, payload.action, payload, payload.priority)

    async def send_message(self, message):
        if message is not None:
            await self.ws.send(message)

    async def consume(self):
        msg_to_consume = await self.incoming.get()
        await self.outgoing.put(msg_to_consume)

    async def produce(self):
        try:
            action = self.queues.get('system.interface', timeout=0.1)
            function = 'on' + action['action'].lower().capitalize()
            getattr(self, function)(*action['action'])
        except (KeyError, AttributeError):
            print('Generate: {0}'.format(action['arguments'].generate()))
            return action['arguments'].generate()
        except queue.Empty:
            pass
        except KeyError:
            payload = Payload(self.name, action['action'], 1, 'Unknown action')
            self.queues.put(self.name, action['action'], payload)
