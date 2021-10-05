#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam
import Localization as loc
from pynput import keyboard

def on_press(key):
    global program_Live
    print('{0} pressed'.format(
        key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        program_Live = False
        return False

program_Live = True
if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    camKeypointX = mp.Array('i', range(11))
    camKeypointZ = mp.Array('i', range(11))

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    camera_process = mp.Process(target=cam.operate_camera, args=(camKeypointX, camKeypointZ))
    localization_process = mp.Process(target=loc.localize, args=(camKeypointX, camKeypointZ))

    camera_process.start()
    localization_process.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    #mingi callbacki/muutuja jälgimise alusel cleanup ja sulgemine
    # Pynputiga keyboard inputide jälgimine
    listener = keyboard.Listener(on_press=on_press, suppressed = True)
    listener.start()

    while program_Live:
        pass

    camera_process.kill()
    localization_process.kill()
    print("Closing down!")