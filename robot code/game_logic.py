import math
from time import sleep, time
from enums import *

#helpers

#combine 2 movement vectors together with some ratio (default 1 to 1)
def combine_moves(move1, move2, p1 = 1, p2 = 1):
    speed = [0,0,0,0]
    for i,v in enumerate(move1):
        speed[i]+= v*p1
    for i,v in enumerate(move2):
        speed[i]+= v*p2
    return speed#returns new movement vector (motor speeds)

def stop():
    return [0, 0, 0, 0]

def linear_velocity(speed, angle, wheel_angle):
    return int(speed * math.cos(math.radians(angle) - math.radians(wheel_angle)))

def move_omni(speed, angle): #generate movement vector with direction and speed
    
    WHEEL_ANGLES = [210, 330, 90]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    return [linear_velocity(speed, angle, wheel_angle) for wheel_angle in WHEEL_ANGLES] + [0]
    #return list(map(linear_velocity,[[speed,angle,210],[speed,angle,330],[speed,angle,90]])) + [0]

def rotate_omni(speed, mults = [1,1,1]): # generate rotation vector with speed
    speed = int(speed)
    return[speed * mult for mult in mults] + [0]

def thrower(speed): # generate rotation vector with speed
    return[0,0,0,speed]

def minimax(v, minim, maxim):
    return max(min(v, maxim),minim)

def rectify_speed(object, max_speed): #changes the biggest wheel speed to be the same as given speed but keeps all ratios the same
    obj = object[0:len(object)-1]
    mx = 0
    for i in obj:
        ai = abs(i)
        if ai > mx:
            mx = ai
    if mx == 0:
        return[0,0,0,0]
    if mx < max_speed:
        return object
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object # returns the correctedmovement vector

def set_speed(target_speeds,speed):
    for i in range(len(speed)):
        target_speeds[i] = speed [i]

def searching(gs, time_of_no_ball, speeds, holding):
    #print(time_of_no_ball.value)
    if holding.value == 1:
        return GameState.search_basket
    if time_of_no_ball.value == 0:
        print("moveto")
        return GameState.moveto
    set_speed(speeds, rotate_omni(30))
    return gs

def moveto(gs, time_of_no_ball, nearest_ball, speeds, holding, grab):
    error = (nearest_ball[0]-424)/4.24
    #print(nearest_ball[0])
    #print('gamestate', gs)

    if gs == GameState.moveto:
        if holding.value == 0:
            if time_of_no_ball.value > 0.5:
                print("moveto to searching")
                grab.value = 0
                return GameState.searching

        elif holding.value == 1:
            gs = GameState.search_basket
            print("ball aquired, searching basket")
        
        if nearest_ball[1] < 200:

            grab.value = 1
            movement_vector = rotate_omni(int(math.floor(error * 0.3)))
            movement_vector = combine_moves(movement_vector, move_omni(60,0))
            speed = 60
            set_speed(speeds, movement_vector)

        else:
            #print(int(math.floor(error ** 1.05 * 0.1)))
            movement_vector = rotate_omni(int(math.floor(error * 0.3)))
            movement_vector = combine_moves(movement_vector, move_omni(60,0))
            speed = 60
            movement_vector = rectify_speed(movement_vector,speed)
            set_speed(speeds, movement_vector)
    else:
        #print(nearest_ball[0])
        #nearest ball here marks the basket
        if nearest_ball[2] == 0:
            set_speed(speeds, rotate_omni(30))
        elif nearest_ball[2] > 2000:
            movement_vector = rotate_omni(int(math.floor(error * 0.3)))
            movement_vector = combine_moves(movement_vector, move_omni(60,0))
            speed = 60
            set_speed(speeds, movement_vector)
        elif nearest_ball[2] < 1500:
            movement_vector = rotate_omni(int(math.floor(error * 0.3)))
            movement_vector = combine_moves(movement_vector, move_omni(-60,0))
            speed = 60
            set_speed(speeds, movement_vector)
        else:
            return GameState.launch
    return gs

def aim(gs, basket, speeds):
    #print(basket[0])
    if basket[0] < 423:
        set_speed(speeds, rotate_omni(-10))
    elif basket[0] > 426:
        set_speed(speeds, rotate_omni(10))
    else:
        print('Throwing!')
        set_speed(speeds,stop())
        return GameState.launch



def pid(x, kp, ki, kd, piddat):
    piddat[0]+=x
    integral = piddat[0]
    derivative = piddat[1]-x
    piddat[1] = x
    return(x * kp + integral * ki + derivative * kd)

'''
def orbit_a(gs, nearest_ball, time_of_no_ball, basket, speeds, pids):
    if nearest_ball[1] > 350 or time_of_no_ball.value > 0.1:
        return GameState.moveto
    
    spd = 20
    
    dif = (basket[0] - nearest_ball[0])/848
    hdelta = nearest_ball[0]/424-1
    vdelta = (math.sin(((nearest_ball[1])*math.pi)/960)) - 0.6

    if (abs(dif)< 0.01 and abs(hdelta)< 0.15 and abs(vdelta)< 0.1):
        return GameState.launch

    movment_vector = move_omni(int(pid(vdelta, 1, 0, 1, pids[0])*spd), 0)
    print(dif,hdelta,  vdelta,basket[0], nearest_ball[0])
    movment_vector = combine_moves(move_omni(int(pid(dif, 4, 0, 0, pids[1])*spd),90),movment_vector)
    movment_vector = combine_moves(rotate_omni(pid(hdelta, 0.4, 0, 0.1, pids[2])*spd, [1,1,0]),movment_vector)
    movment_vector = rectify_speed(movment_vector, 20)
    set_speed(speeds,movment_vector)
    return gs


def orbit(gs, nearest_ball, time_of_no_ball, basket, speeds): #old orbiter code
    #print("o", nearest_ball[0],nearest_ball[1],nearest_ball[2])
    if nearest_ball[1] > 300 or time_of_no_ball.value > 0.1:
        return GameState.moveto
    
    tgt = [basket[0], basket[1], basket[2]]

    spd = 20
    if abs(tgt[0] - 424) < 60:
        spd = 3
    elif abs(tgt[0] - 424) < 424:
        spd = 5
    

    movement_vector = move_omni(minimax((nearest_ball[1]-160)*0.18,-spd,spd),0)
    movement_vector = combine_moves(movement_vector, rotate_omni(minimax((nearest_ball[0]-424)*0.08, -spd,spd), [1,1,0]))
    #movement_vector = combine_moves(movement_vector, rotate_omni(minimax((nearest_ball[0]-424), 3,-3), [1,1,0]))
    #movement_vector = combine_moves(movement_vector, move_omni(max(min((nearest_ball[0]-424)*0.1, 3),-3),90))
    #print(movement_vector)
    if abs(tgt[0] - 424) <= 10 and abs(nearest_ball[0]-424) <= 10:
        gs = GameState.launch
    elif tgt[0] > 424:
        movement_vector = combine_moves(movement_vector, move_omni(spd, 90))
    elif tgt[0] < 424:
        movement_vector = combine_moves(movement_vector, move_omni(-spd, 90))
    
    #movement_vector = rectify_speed(movement_vector, 20)
    #print(movement_vector)
    set_speed(speeds,movement_vector)
    return gs
'''

def launch(gs, speeds, tgt, holding, launchenable, hoidja):
    hoidja.value = 0
    if holding.value == 0:
        return GameState.searching

    dist = tgt[2]
    throwerSpeed = int(round(3500 + dist*0.45))
    throw = thrower(throwerSpeed)
    set_speed(speeds, throw)
    launchenable.value = 1

def main(nearest_ball, speeds, state, time_of_no_ball, basket, holding, grab, launchenable):# main function of movement controller 
    sleep(0.5)

    gs = GameState.searching

    last_time = time()
    while True:
        current_time = time()
        delta = current_time-last_time
        last_time = current_time

        if (state.value != State.automatic):
            continue
        #print(nearest_ball[0], nearest_ball[1],nearest_ball[2])
        if  gs == GameState.searching:
            gs = searching(gs, time_of_no_ball, speeds, holding)
        elif gs == GameState.moveto:
            gs = moveto(gs, time_of_no_ball, nearest_ball, speeds, holding, grab)
        elif gs == GameState.search_basket:
            gs = moveto(gs, time_of_no_ball, basket, speeds, holding, grab)

        elif gs == GameState.orbit:
            gs = aim(gs, basket, speeds)
        elif gs == GameState.launch:
            gs = launch(gs, speeds, basket, holding, launchenable, grab)
        else:
            gs = GameState.searching
            launchenable.value = 0
            print("reset")




# 379 - 600
# 407 - 700
# 418 - 800
