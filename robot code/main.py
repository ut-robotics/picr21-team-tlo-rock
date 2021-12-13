#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam
import Localization as loc
import game_logic as gl
import shooting_calibration as sc
import movement_controller as mc
import manual_control as man
import numpy as np
from pynput import keyboard
from functools import partial
from enums import *

def on_press(context, key):
    running, state, manual_inputs = context
    keymap = ['u', 'i', 'o', 'j', 'l', 'k', 'n']

    #print('{0} pressed'.format(key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        running.value = 0
        return False
    if state.value in {State.remote, State.calibration}:
        for index, value in enumerate(keymap):
            if key == keyboard.KeyCode.from_char(value):
                manual_inputs[index] = 1

def on_release(context, key):
    state, manual_inputs = context
    keymap = ['u', 'i', 'o', 'j', 'l', 'k', 'n']

    if state.value in {State.remote, State.calibration}:
        for index, value in enumerate(keymap):
            if key == keyboard.KeyCode.from_char(value):
                manual_inputs[index] = 0

    if state.value == State.automatic and key == keyboard.KeyCode.from_char('m'):
        state.value = State.remote
        print('Switching to manual control!')

    elif state.value == State.remote and key == keyboard.KeyCode.from_char('m'):
        state.value = State.automatic
        print('Switching to automatic mode!')
    
    if state.value == State.calibration and key == keyboard.KeyCode.from_char('c'):
        state.value = State.remote
        print('Switching to manual control!')

    elif state.value == State.remote and key == keyboard.KeyCode.from_char('c'):
        state.value = State.calibration
        print('Switching to calibration mode!')
    

if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    ballKeypointX = mp.Array('i', np.zeros(11, dtype=int))
    ballKeyPointY = mp.Array('i', np.zeros(11, dtype=int))
    ballKeyPointZ = mp.Array('i', np.zeros(11, dtype=int))
    BasketCoords = mp.Array('i', np.zeros(3, dtype=int))
    nearest_ball = mp.Array('i', np.zeros(3, dtype=int))
    speeds = mp.Array('i', np.zeros(4, dtype=int))
    running = mp.Value('i', 1)
    state = mp.Value('i', State.remote)
    attacking = mp.Value('i', Side.pink)
    noball = mp.Value('f', 0) #float noball is the time since last ball was detected 
    manual_inputs = mp.Array('i', np.zeros(7, dtype=int))

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    camera_process = mp.Process(target=cam.operate_camera, args=(ballKeypointX, ballKeyPointY, ballKeyPointZ, attacking, BasketCoords))
    localization_process = mp.Process(target=loc.localize, args=(ballKeypointX, ballKeyPointY, ballKeyPointZ, nearest_ball, noball))
    game_logic_process = mp.Process(target=gl.main, args=(nearest_ball, speeds, state, noball,BasketCoords))
    calibration_process = mp.Process(target=sc.main, args=(speeds, state, BasketCoords, manual_inputs))
    movement_controller_process = mp.Process(target=mc.main, args=(speeds, state, running))
    manual_override_process = mp.Process(target=man.manualdrive, args=(manual_inputs, state, speeds))

    camera_process.start()
    localization_process.start()
    game_logic_process.start()
    movement_controller_process.start()
    manual_override_process.start()
    calibration_process.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    # Roboti kasutaja sisendite võimaldamine
    # Pynputiga keyboard input-ide jälgimine
    listener = keyboard.Listener(on_press=partial(on_press, (running, state, manual_inputs)), 
                                on_release=partial(on_release, (state, manual_inputs)))
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
    calibration_process.kill()
    print("Closing down!")
