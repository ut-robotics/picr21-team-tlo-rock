import serial
import struct
from serial.tools import list_ports
from time import sleep

def send_ms(speeds): #unpack motorspeeds
    return send_motorspeeds(speeds[0],speeds[1],speeds[2],speeds[3]) #returns motor data

def send_motorspeeds(m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack('<hhhHBH', m1, m2, m3, thrower, 0, 0xAAAA))
    size = struct.calcsize('<hhhH')
    data = ser.read(size)
    values = struct.unpack('<hhhH',data)
    for i in values:
        print(i)
    return values #returns motor data

    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

def combine_moves(move1, p1, move2, p2):
    speed = [0,0,0,0]
    for i,v in enumerate(move1):
        ret[i]+= v*p1
    for i,v in enumerate(move2):
        ret[i]+= v*p2
    return speed

def move_forward(speed): #same as move3
    return [-speed, speed, 0, 0]

def move_3(speed):
    return [-speed, speed, 0, 0]

def move_2(speed):
    return [speed, 0, -speed, 0]

def move_1(speed):
    return [0, -speed, speed, 0]

#port =list(list_ports.comports())[0]
#print(port.name)
try:
    port='/dev/ttyACM0'
    ser = serial.Serial(port, baudrate=115200, timeout=3)
    for i in range (2):
        print('----')
        send_ms(combine_moves(move_2(10), 2,move_3(10) , 1))
        sleep(0.05)
except Exception as e:
    print(e)
ser.close()