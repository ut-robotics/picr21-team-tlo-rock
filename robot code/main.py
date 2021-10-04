#!/usr/bin/env python
import multiprocessing as mp
import Camera as cam

if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    num = mp.Value('d', 0.0)
    arr = mp.Array('i', range(10))

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    p = mp.Process(target=cam.operate_camera, args=())

    #p.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    #mingi callbacki/muutuja jälgimise alusel cleanup ja sulgemine
    #p.kill()