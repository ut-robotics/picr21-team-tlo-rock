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

def linear_velocity(values):
    return int(values[0] * math.cos(math.radians(values[1]) - math.radians(values[2])))

def move_omni(speed, angle): #generate movement vector with direction and speed
    
    WHEEL_ANGLES = [210, 330, 90]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    return [linear_velocity([speed, angle, wheel_angle]) for wheel_angle in WHEEL_ANGLES] + [0]
    #return list(map(linear_velocity,[[speed,angle,210],[speed,angle,330],[speed,angle,90]])) + [0]

def rotate_omni(speed): # generate rotation vector with speed
    speed = int(speed)
    return[speed,speed,speed,0]

def thrower(speed): # generate rotation vector with speed
    return[0,0,0,speed]

def rectify_speed(object, max_speed): #changes the biggest wheel speed to be the same as given speed but keeps all ratios the same
    obj = object[0:len(object)-1]
    mx = 0
    for i in obj:
        if abs(i) > mx:
            mx = abs(i)
    if mx == 0:
        return[0,0,0,0]
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object # returns the correctedmovement vector

def set_speed(target_speeds,speed):
    for i in range(len(speed)):
        target_speeds[i] = speed [i]


def main(nearest_ball, speeds, state, noball, basket):# main function of movement controller 
    sleep(0.5)
    #while True:
    #    set_speed(speeds, thrower(550)) 
    #    print(speeds[0],speeds[1],speeds[2],speeds[3])
    
    # pid constants
    #Kp = 0.8
    #Ki = 0.9
    #Kd = 0.6
    gls = GameState.searching

    launchdelay = 0

    gs = GameState.searching

    tgt = [0,0,0]

    last_time = time()
    while True:
        current_time = time()
        delta = current_time-last_time
        last_time = current_time

        if (state.value != State.automatic):
            continue
        if  gs == GameState.searching:
            if noball.value == 0:
                gs = GameState.moveto
            set_speed(speeds, rotate_omni(10))
        if gs == GameState.moveto:

            if noball.value > 0.5:
                gs = GameState.searching

            #print(nearest_ball[0], nearest_ball[1])
            if nearest_ball[0] != 0: # failsafe
                error = (nearest_ball[0]-424)/4.24
                
                if nearest_ball[1] < 200:
                    gs = GameState.orbit
                else:
                    #print(int(math.floor(error ** 1.05 * 0.1)))
                    movement_vector = rotate_omni(int(math.floor(error * 0.04)))
                    movement_vector = combine_moves(movement_vector, move_omni(25,0))
                    speed = 50
                    if nearest_ball[1] < 1000:
                        speed = 30
                    movement_vector = rectify_speed(movement_vector,speed)
                    set_speed(speeds, movement_vector)
            
            else:
                set_speed(speeds, rotate_omni(10))
        
        if gs == GameState.orbit:
            if nearest_ball[1] > 300 or noball.value > 0.5:
                gs = GameState.moveto
            
            tgt = [basket[0], basket[1], basket[2]]
            #print("basket",basket[0],basket[1],basket[2])
            #if noball.value > 0.5:
            #    gs = GameState.searching
            #print(nearest_ball[0],nearest_ball[1])
            # distance from robot tgt 130
            # side to side tgt 424,425

            spd = 20
            if abs(tgt[0] - 424) < 424:
                spd = 5
            if abs(tgt[0] - 424) < 60:
                spd = 3

            movement_vector = move_omni(max(min((nearest_ball[1]-160)*0.18,spd),-spd),0)
            movement_vector = combine_moves(movement_vector, rotate_omni(max(min((nearest_ball[0]-424)*0.04, spd),-spd)))
            movement_vector = combine_moves(movement_vector, rotate_omni(max(min((nearest_ball[0]-424), 3),-3)))
            #movement_vector = combine_moves(movement_vector, move_omni(max(min((nearest_ball[0]-424)*0.1, 3),-3),90))
            if abs(tgt[0] - 424) <= 5 and abs(nearest_ball[0]-424) <= 5:
                gs = GameState.launch
            elif tgt[0] > 424:
                movement_vector = combine_moves(movement_vector, move_omni(spd, 90))
                combine_moves(movement_vector, rotate_omni(-5))
            elif tgt[0] < 424:
                movement_vector = combine_moves(movement_vector, move_omni(-spd, 90))
                combine_moves(movement_vector, rotate_omni(5))
            
            #movement_vector = rectify_speed(movement_vector, 20)
            #print(movement_vector)
            set_speed(speeds,movement_vector)
        if gs == GameState.launch:
            if launchdelay < 1:
                set_speed(speeds,stop())
                launchdelay += delta
                #print(tgt)
                if abs(tgt[0] - 424 > 3 and abs(nearest_ball[0]-424) > 2 and abs(nearest_ball[1]-160) < 2):
                    gs = GameState.orbit
                    launchdelay = 0
            else:
                launchdelay = 0
                movement_vector = move_omni(5,0)
                #print(int(0.05*(tgt[1]-350)**2+560)) # 0.05\left(x-350\right)^{2}\ +560
                movement_vector = combine_moves(movement_vector, thrower(int(0.05*(tgt[1]-350)**2+570)))
                #movement_vector = combine_moves(movement_vector, thrower(int(0.000006*(tgt[1]-340)**4+560)))
                #movement_vector = combine_moves(movement_vector, thrower(int(0.00038*(tgt[1]-344)**3+610)))
                set_speed(speeds,movement_vector)
                sleep(3)
                gs = GameState.searching




# 379 - 600
# 407 - 700
# 418 - 800
