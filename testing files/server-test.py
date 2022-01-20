#!/usr/bin/env python

import asyncio
import websockets
import json
import time

async def echo(websocket):
    refcomm = '{"signal": "stop", "targets":  ["Io", "TLOROCK"], "baskets": ["magenta", "blue"]}'

    while True:
        await websocket.send(refcomm)
        time.sleep(5)

async def main():
    async with websockets.serve(echo, "localhost", 8765, ping_interval=None):
        await asyncio.Future()  # run forever

asyncio.run(main())