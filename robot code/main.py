#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam
import Localization as loc
import movement_logic as ml
import movement_controller as mc
import manual_control as man
from pynput import keyboard

def on_press(key):
    global running, state, manual_inputs
    print('{0} pressed'.format(key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        running.value = 0
        return False
    elif key == keyboard.Key.num_lock:
        state = 2
        print('Switching to manual control!')
    elif key == keyboard.Key.insert:
        state = 1
        print('Switching to logic controller!')
    elif state == 2:
        if key == keyboard.Key.home:
            manual_inputs[0] = 1
        elif key == keyboard.Key.up:
            manual_inputs[1] = 1
        elif key == keyboard.Key.page_up:
            manual_inputs[2] = 1
        elif key == keyboard.Key.left:
            manual_inputs[3] = 1
        elif key == keyboard.Key.right:
            manual_inputs[4] = 1
        elif key == keyboard.Key.down:
            manual_inputs[5] = 1
        elif key == keyboard.Key.end:
            manual_inputs[6] = 1
            manual_inputs[0] = 0
            manual_inputs[1] = 0
            manual_inputs[2] = 0
            manual_inputs[3] = 0
            manual_inputs[4] = 0
            manual_inputs[5] = 0

def on_release(key):
    global manual_inputs, state
    if state == 2:
        if key == keyboard.Key.home:
            manual_inputs[0] = 0
        elif key == keyboard.Key.up:
            manual_inputs[1] = 0
        elif key == keyboard.Key.page_up:
            manual_inputs[2] = 0
        elif key == keyboard.Key.left:
            manual_inputs[3] = 0
        elif key == keyboard.Key.right:
            manual_inputs[4] = 0
        elif key == keyboard.Key.down:
            manual_inputs[5] = 0
        elif key == keyboard.Key.end:
            manual_inputs[6] = 0
    

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
    movement_logic_process = mp.Process(target=ml.main, args=(nearest_ball, speeds))
    movement_controller_process = mp.Process(target=mc.main, args=(speeds, state, running))
    manual_override_process = mp.Process(target=man.manualdrive, args=(manual_inputs, state, speeds))

    camera_process.start()
    localization_process.start()
    movement_logic_process.start()
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
    movement_logic_process.kill()
    manual_override_process.kill()
    #print('logic killed')
    movement_controller_process.kill()
    #print('moving killed')
    print("Closing down!")