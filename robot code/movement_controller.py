import serial
import struct
import math
from time import sleep

#helpers

def send_ms(ser,speeds): #unpacks motorspeeds
    return send_motorspeeds(ser,speeds[0],speeds[1],speeds[2],speeds[3]) #returns motor data

def send_motorspeeds(ser,m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack('<hhhHBH', m1, m2, m3, thrower, 0, 0xAAAA))
    size = struct.calcsize('<hhhH')
    data = ser.read(size)
    values = struct.unpack('<hhhH',data)
    return values #returns motor data

    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

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

def rectify_speed(object, max_speed): #changes the biggest wheel speed to be the same as given speed but keeps all ratios the same
    obj = object[0:len(object)-1]
    mx = 0
    for i in obj:
        if abs(i) > mx:
            mx = abs(i)
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object # returns the correctedmovement vector

def main(nearest_ball, running):# main function of movement controller
    robot_speed = 100 # robots speed
    ser = None    #create serial connection
    try:
        port='/dev/ttyACM1'
        ser = serial.Serial(port, baudrate=115200, timeout=3)

        last_ball = []
        stop_counter = 0

        while True:

            #print(running.value)
            #print(nearest_ball[0], nearest_ball[1])
            if running.value == 0:# stop if no longer runing
                break
            if nearest_ball[0] != 0: # failsafe
                if nearest_ball[1] < 400:
                    send_ms(ser, stop())
                else:
                    if nearest_ball == last_ball:
                        stop_counter += 1
                        if stop_counter > 30:
                            send_ms(ser, stop())
                            continue
                    last_ball = nearest_ball
                    stop_counter = 0
                    
                    p_val = (nearest_ball[0]-320)/320 #p controller
                    #print(p_val)
                    movement_vector = combine_moves(move_omni(90, 0),move_omni(p_val*10, -90)) #calculate movement vector trying to center the ball
                    turning_vector = combine_moves (movement_vector, rotate_omni(p_val*50)) # calculate turning vector trying to turn toward the ball
                    wheel_speeds = rectify_speed(turning_vector , robot_speed) #set movement speed
                    motor_data = send_ms(ser,wheel_speeds) # execute movement
    except Exception as e:
        print(e)
    if ser != None:
        ser.close()
    running.value = -1
    
