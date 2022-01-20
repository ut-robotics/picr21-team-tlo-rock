#!/usr/bin/env python

import asyncio
import websockets
import json

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        print(await websocket.recv())

asyncio.run(hello())