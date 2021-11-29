from game_logic import *
from enums import *
from time import sleep

def main( speeds, state, basket, input):
    sleep(2)
    tgt = [0,0,0]
    ts = 600

    thrower_lock = True
    snap_lock = True

    tdrec = 0
    tlcrec = 0
    tsrec = 0

    while True:
        movement_vector = [0,0,0,0]
        
        sleep(0.01)
        if state.value != State.calibration:
            continue
        tgt = [basket[0], basket[1], basket[2]]
        spd = 20

        spd = min(max(int((abs(tgt[0] - 424)/424) * 10),1),10)

        #print(tgt[0] - 424, spd)
        if abs(tgt[0] - 424) <= 2:
            movement_vector = [0,0,0,0]
            pass
        
        if (tgt[0] - 424 > 0):
            #movement_vector = rotate_omni(spd)
            movement_vector = combine_moves(move_omni(spd, 90), movement_vector)
            pass
        if (tgt[0] - 424 < 0):
            #movement_vector = rotate_omni(-spd)
            movement_vector = combine_moves(move_omni(-spd, 90), movement_vector)
            pass
        movement_vector = combine_moves(move_omni(5, 0), movement_vector)
        #print(input[1])
        if input[5] != 0:
            ts -= 1
            ts = max(0, ts)
            #print(ts)
        if input[1] != 0:
            ts += 1
            ts = min(2048, ts)
            #print(ts)
        if input[3] != 0 and thrower_lock:
            ts -= 1
            ts = max(0, ts)
            #print(ts)
            thrower_lock = False
        if input[4] != 0 and thrower_lock:
            ts += 1
            ts = min(2048, ts)
            #print(ts)
            thrower_lock = False
        if input[4] == 0 and input[3] == 0 and not thrower_lock:
            thrower_lock = True
        if input[0] != 0:
            tdrec = tgt[2]
            tlcrec = tgt[1]
            tsrec = ts
        if input[2] != 0 and snap_lock:
            print("snap")
            file_object = open('shootingdata.txt', 'a')
            file_object.write((str(tsrec)+ " " +str(tdrec)+ " " +str(tlcrec)+"\n"))
            file_object.close()
            snap_lock = False
        if input[6] == 0:
            snap_lock = True

        movement_vector = combine_moves(movement_vector, thrower(ts))
        #print(movement_vector)
        if input[6] != 0:
            set_speed(speeds,movement_vector)
            