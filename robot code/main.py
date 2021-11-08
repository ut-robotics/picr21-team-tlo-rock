#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam
import Localization as loc
import game_logic as gl
import movement_controller as mc
import manual_control as man
from pynput import keyboard
from enums import *

def getARunningStateWithManualInputs():
    return running, state, manual_inputs

def on_press(key):
    running, state, manual_inputs = getARunningStateWithManualInputs()
    keymap = ['u', 'i', 'o', 'j', 'l', 'k', 'n']

    #print('{0} pressed'.format(key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        running.value = 0
        return False
    elif state.value == State.automatic and key == keyboard.KeyCode.from_char('m'):
        state.value = State.remote
        print('Switching to manual control!')
    elif state.value == State.remote and key == keyboard.KeyCode.from_char('m'):
        state.value = State.automatic
        print('Switching to automatic mode!')
    elif state.value == State.remote:
        for index, value in enumerate(keymap):
            if key == keyboard.KeyCode.from_char(value):
                manual_inputs[index] = 1

def on_release(key):
    _, state, manual_inputs = getARunningStateWithManualInputs()
    keymap = ['u', 'i', 'o', 'j', 'l', 'k', 'n']

    if state.value == 2:
        for index, value in enumerate(keymap):
            if key == keyboard.KeyCode.from_char(value):
                manual_inputs[index] = 0
    

if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    camKeypointX = mp.Array('i', range(11))
    camKeypointZ = mp.Array('i', range(11))
    nearest_ball = mp.Array('i', range(2))
    speeds = mp.Array('i', [i-i for i in range(4)])
    running = mp.Value('i', 1)
    state = mp.Value('i', 1)
    manual_inputs = mp.Array('i', [i-i for i in range(7)])

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    camera_process = mp.Process(target=cam.operate_camera, args=(camKeypointX, camKeypointZ))
    localization_process = mp.Process(target=loc.localize, args=(camKeypointX, camKeypointZ, nearest_ball))
    game_logic_process = mp.Process(target=gl.main, args=(nearest_ball, speeds, state))
    movement_controller_process = mp.Process(target=mc.main, args=(speeds, state, running))
    manual_override_process = mp.Process(target=man.manualdrive, args=(manual_inputs, state, speeds))

    camera_process.start()
    localization_process.start()
    game_logic_process.start()
    movement_controller_process.start()
    manual_override_process.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    #mingi callbacki/muutuja jälgimise alusel cleanup ja sulgemine
    # Pynputiga keyboard inputide jälgimine
    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppressed = True)
    listener.start()

    while running.value != -1:
        pass

    camera_process.kill()
    #print('cam killed')
    localization_process.kill()
    #print('loc killed')
    game_logic_process.kill()
    manual_override_process.kill()
    #print('logic killed')
    movement_controller_process.kill()
    #print('moving killed')
    print("Closing down!")
    print("Closing down!")