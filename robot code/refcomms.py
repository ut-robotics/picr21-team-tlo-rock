import asyncio
import websockets
import json
from enums import *

async def refcommClient(robotState, attackingSide):
    async with websockets.connect("ws://localhost:8765", ping_interval=None) as websocket:
        robotName = 'TLOROCK'
        while True:
            refcomm = await websocket.recv()
            print('Signal recieved...')
            refdict = json.loads(refcomm)
            if robotName in refdict['targets']:
                if refdict['signal'] == 'start':
                    if refdict['baskets'][refdict['targets'].index(robotName)] == 'blue':
                        attackingSide = Side.blue
                    else:
                        attackingSide = Side.pink
                    robotState = State.automatic
                    print('Starting competition!')

                elif refdict['signal'] == 'stop':
                    robotState = State.remote
                    print('Stopping competition! Switching to manual control...')
            else:
                print('Signal not directed at', robotName)

            print(robotState, attackingSide)


def refclient(state, attacking):
    asyncio.run(refcommClient(state, attacking))

if __name__ == '__main__':
    refclient(5, 5)