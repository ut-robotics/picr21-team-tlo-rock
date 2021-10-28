from cv2 import integral
import serial
import struct
import math
from time import sleep, time

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
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    return list(map(linear_velocity,[[speed,angle,210],[speed,angle,330],[speed,angle,90]])) + [0]

def rotate_omni(speed): # generate rotation vector with speed
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


def main(nearest_ball, speeds, state):# main function of movement controller
    robot_speed = 100 # robots speed
    sleep(3)
    #while True:
    #    set_speed(speeds, thrower(800)) 
    #    print(speeds[0],speeds[1],speeds[2],speeds[3])
    
    # pid constants
    #Kp = 0.8
    #Ki = 0.9
    #Kd = 0.6

    last_ball = 0
    stop_counter = 0
    l_time = time()

    

    while True:

        tme = time()
        delta = tme - l_time
        l_time = tme

        sleep(0.01)
        #print("delta", delta)
        if (state.value != 1):
            continue

        #print(nearest_ball[0], nearest_ball[1])
        if nearest_ball[0] != 0: # failsafe
            if nearest_ball[1] < 500:
                set_speed(speeds, stop())
                pass
            else:
                error = (nearest_ball[0]-320)/3.2
                #print(int(math.floor(error ** 1.05 * 0.1)))
                movement_vector = rotate_omni(int(math.floor(error * 0.9)))
                movement_vector = combine_moves(movement_vector, move_omni(25,0))
                speed = 80
                if nearest_ball[1] < 800:
                    speed = 25
                movement_vector = rectify_speed(movement_vector,speed)
                set_speed(speeds, movement_vector)
        
        #set_speed(speeds, rotate_omni(10))
    
