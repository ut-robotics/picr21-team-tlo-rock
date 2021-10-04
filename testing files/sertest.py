import serial
import struct
import math
from time import sleep

def send_ms(speeds): #unpack motorspeeds
    return send_motorspeeds(speeds[0],speeds[1],speeds[2],speeds[3]) #returns motor data

def send_motorspeeds(m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack('<hhhHBH', m1, m2, m3, thrower, 0, 0xAAAA))
    size = struct.calcsize('<hhhH')
    data = ser.read(size)
    values = struct.unpack('<hhhH',data)
    return values #returns motor data

    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

def combine_moves(move1, p1, move2, p2):
    speed = [0,0,0,0]
    for i,v in enumerate(move1):
        speed[i]+= v*p1
    for i,v in enumerate(move2):
        speed[i]+= v*p2
    return speed

def move_forward(speed): #same as move3
    return [-speed, speed, 0, 0]

def move_3(speed):
    return [-speed, speed, 0, 0]

def move_2(speed):
    return [speed, 0, -speed, 0]

def move_1(speed):
    return [0, -speed, speed, 0]

def thrower(speed):
    return [0,0,0,speed]

def move_omni(speed, angle): 
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    
    return [int(speed * math.cos(math.radians(angle) - math.radians(210))), int(speed * math.cos(math.radians(angle) - math.radians(300))), int(speed * math.cos(math.radians(angle) - math.radians(90))), 0]

def rotate_omni(speed): 
    return[speed,speed,speed,0]

def rectify_speed(object, max_speed): 
    mx = (max(object[0:len(object)-1]))
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object

#port =list(list_ports.comports())[0]
#print(port.name)
ser = None
try:
    port='/dev/ttyACM0'
    ser = serial.Serial(port, baudrate=115200, timeout=3)
    for i in range (10):
        print('----')
        send_ms(rectify_speed(combine_moves(move_omni(20, 0),1,rotate_omni(10),1),20))
        sleep(0.05)
except Exception as e:
    print(e)
if ser != None:
    ser.close()