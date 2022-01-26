import asyncio
import websockets
import json
from enums import *

async def refcommClient(robotState, attackingSide):
    
    robotName = 'tlo_rock'
    connectTo = 'ws://192.168.3.220:8111'

    async with websockets.connect(connectTo, ping_interval=None) as websocket:
        while True:
            refcomm = await websocket.recv()
            print('Signal recieved...')
            refdict = json.loads(refcomm)
            print(refdict['targets'])
            if refdict['signal'] == 'start':
                print(refdict['baskets'])
            if robotName in refdict['targets']:
                if refdict['signal'] == 'start':
                    if refdict['baskets'][refdict['targets'].index(robotName)] == 'blue':
                        attackingSide.value = Side.blue
                    elif refdict['baskets'][refdict['targets'].index(robotName)] == 'magenta':
                        attackingSide.value = Side.pink
                    robotState.value = State.automatic
                    print('Starting competition!')

                elif refdict['signal'] == 'stop':
                    robotState.value = State.remote
                    print('Stopping competition! Switching to manual control...')
            else:
                print('Signal not directed at', robotName)

            #print(robotState.value, attackingSide)


def refclient(state, attacking):
    asyncio.run(refcommClient(state, attacking))

if __name__ == '__main__':
    refclient(5, 5)