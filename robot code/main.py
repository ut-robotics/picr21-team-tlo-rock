import multiprocessing as mp
import Camera as cam

if __name__ == '__main__':
    #______________________________MUUTUJATE LOOMISE PLOKK_________________________________
    keypointX = mp.Array('i', range(11))
    keypointZ = mp.Array('i', range(11))

    #________________PROTSESSIDE ALUSTAMINE JA MUUTUJATE KAASA ANDMINE_____________________
    p = mp.Process(target=cam.operate_camera, args=(keypointX, keypointZ))

    #p.start()

    #_________________________________MUUD ADMIN TEGEVUSED__________________________________
    #mingi callbacki/muutuja jälgimise alusel cleanup ja sulgemine
    #p.kill()