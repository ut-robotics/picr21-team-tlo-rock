import movement_logic as ml

def manualdrive(inputarray, control_state, speeds):
    while True:
        if control_state == 2:
            #inputarray-home, up, pgup, left, right, down, end
            
            if inputarray[6]:
                ml.set_speed(speeds, ml.stop())

            movement_vector = ml.combine_moves(ml.move_omni(100*(inputarray[1]-inputarray[5]), 0)), ml.move_omni(70, 90*(inputarray[4]-inputarray[3]))) #calculate movement vector
            turning_vector = ml.combine_moves (movement_vector, ml.rotate_omni(50*(inputarray[2]-inputarray[0]))) # calculate turning vector
            wheel_speeds = ml.rectify_speed(turning_vector, 100) #set movement speed
            #print(wheel_speeds)
            ml.set_speed(speeds, wheel_speeds)
        else:
            pass