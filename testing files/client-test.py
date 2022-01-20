#!/usr/bin/env python

import asyncio
import websockets
import json

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            refcomm = await websocket.recv()
            refdict = json.loads(refcomm)
            print(refdict.keys())

asyncio.run(hello())