import game_logic as ml
from enums import *

def manualdrive(inputarray, control_state, speeds):
    while True:
        #print(control_state.value)
        if control_state.value == State.remote:
            #inputarray-u, i, o, j, l, k, n
            
            if inputarray[6]:
                ml.set_speed(speeds, ml.stop())
                continue
            #inputarray[3] = 1

            movement_vector = ml.combine_moves(ml.move_omni(100*(inputarray[1]-inputarray[5]), 0), ml.move_omni(100*(inputarray[4]-inputarray[3]), 90)) #calculate movement vector
            turning_vector = ml.combine_moves (movement_vector, ml.rotate_omni(5*(inputarray[0]-inputarray[2]), [1,1,0])) # calculate turning vector
            wheel_speeds = ml.rectify_speed(turning_vector, 20) #set movement speed
            #wheel_speeds = ml.combine_moves(wheel_speeds,ml.thrower(600)) #activate thrower
            #print(wheel_speeds)
            #print(inputarray[0],inputarray[1],inputarray[2],inputarray[3],inputarray[4],inputarray[5],inputarray[6])
            ml.set_speed(speeds, wheel_speeds)
        else:
            pass