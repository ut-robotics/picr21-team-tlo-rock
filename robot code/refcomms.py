import asyncio
import websockets
import json
from enums import *

async def refcommClient(robotState, attackingSide):
    
    robotName = 'TLOROCK'
    connectTo = 'ws://192.168.3.220:8220'

    async with websockets.connect(connectTo, ping_interval=None) as websocket:
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
    while True:
        try:
            asyncio.run(refcommClient(state, attacking))
        except:
            print('Ref not reached!')
            pass

if __name__ == '__main__':
    refclient(5, 5)