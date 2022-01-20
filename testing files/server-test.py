#!/usr/bin/env python

import asyncio
import websockets
import json

async def echo(websocket):
    refcomm = {
                "signal": "start",
                "targets":  ["Io", "001TRT"],
                "baskets": ["magenta", "blue"]
            }

    async for message in websocket:
        await websocket.send(refcomm)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())