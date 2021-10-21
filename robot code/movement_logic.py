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

def move_omni(speed, angle): #generate movement vector with direction and speed
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    return [int(speed * math.cos(math.radians(angle) - math.radians(210))), int(speed * math.cos(math.radians(angle) - math.radians(330))), int(speed * math.cos(math.radians(angle) - math.radians(90))), 0]

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
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object # returns the correctedmovement vector

def set_speed(target_speeds,speed):
    for i in range(len(speed)):
        target_speeds[i] = speed [i]

def main(nearest_ball, speeds):# main function of movement controller
    robot_speed = 100 # robots speed
    sleep(3)
#    while True:
#        set_speed(speeds, thrower(800)) 
#        print(speeds[0],speeds[1],speeds[2],speeds[3])
    
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
        #print(delta)

        if nearest_ball[0] != 0: # failsafe
            if nearest_ball[1] < 350:
                set_speed(speeds, stop())
                pass
            else:
                error = (nearest_ball[0]-320)/320*100
                print(error, nearest_ball[0])
    
