#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam
import Localization as loc
import movement_controller as mc
from pynput import keyboard

def on_press(key):
    global program_Live, running
    print('{0} pressed'.format(key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        running.value = 0
        return False

if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    camKeypointX = mp.Array('i', range(11))
    camKeypointZ = mp.Array('i', range(11))
    nearest_ball = mp.Array('i', range(2))
    running = mp.Value('i', 1)

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    camera_process = mp.Process(target=cam.operate_camera, args=(camKeypointX, camKeypointZ))
    localization_process = mp.Process(target=loc.localize, args=(camKeypointX, camKeypointZ, nearest_ball))
    movement_controller = mp.Process(target=mc.main, args=(nearest_ball, running))

    camera_process.start()
    localization_process.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    #mingi callbacki/muutuja jälgimise alusel cleanup ja sulgemine
    # Pynputiga keyboard inputide jälgimine
    listener = keyboard.Listener(on_press=on_press, suppressed = True)
    listener.start()

    while running.value != -1:
        pass

    camera_process.kill()
    localization_process.kill()
    print("Closing down!")