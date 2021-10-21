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
    while True:
        set_speed(speeds, thrower(2047)) 
        #print(speeds[0],speeds[1],speeds[2],speeds[3])
    
    # pid constants
    Kp = 0.8
    Ki = 0.9
    Kd = 0.6

    last_ball = 0
    stop_counter = 0

    integral = 0
    l_p_val = 0
    l_time = 0

    while True:
        
        tme = time()
        delta = tme - l_time
        l_time = tme

        if nearest_ball[0] != 0: # failsafe
            if nearest_ball[1] < 400:
                set_speed(speeds, stop())
                pass
            else:
                if nearest_ball[1] == last_ball:
                    stop_counter += 1
                    if stop_counter > 100:
                        set_speed(speeds, rotate_omni(20))
                        continue
                else :
                    stop_counter = 0
                if stop_counter < 200:
                    last_ball = nearest_ball[1]
                    
                    p_val = (nearest_ball[0]-320)/320 #p controller

                    slope = p_val-l_p_val
                    l_p_val = p_val

                    integral += p_val*delta

                    pid = p_val * Kp + integral * Ki + slope * Kd # pid controller
                    #print(pid)

                    #print(p_val)
                    movement_vector = combine_moves(move_omni(min(60,int( nearest_ball[1]-300 / 4.5)), 0),move_omni(p_val*0, -90)) #calculate movement vector trying to center the ball
                    turning_vector = combine_moves (movement_vector, rotate_omni(pid*40)) # calculate turning vector trying to turn toward the ball
                    wheel_speeds = rectify_speed(turning_vector , robot_speed) #set movement speed

                    print(wheel_speeds)

                    set_speed(speeds, wheel_speeds)
    
